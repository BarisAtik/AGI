"""Breadth-First Search agent for ARC-AGI-3.

Strategy:
  Explores the action space level-by-level, finding the shortest action
  sequence to reach a win state. Uses undo chains to navigate between
  branches since the environment is sequential (no cloning).

  Trade-off vs DFS: BFS guarantees shortest path but uses more memory
  and requires more backtracking steps to navigate the implicit tree.
"""

from __future__ import annotations

import hashlib
from collections import deque
from dataclasses import dataclass, field

from .agent import Agent
from .structs import ActionWithData, FrameData, GameAction, GameState, SIMPLE_ACTIONS


def _hash_frame(frame: FrameData) -> str:
    if frame.grid is not None:
        content = str(frame.grid)
    else:
        content = frame.render
    content += f"|lv={frame.levels_completed}"
    return hashlib.md5(content.encode(), usedforsecurity=False).hexdigest()[:16]


@dataclass
class BFSNode:
    """A node in the BFS tree, storing the path of actions to reach it."""

    state_hash: str
    action_path: list[GameAction]  # actions from root to this node
    depth: int


class BFSAgent(Agent):
    """Breadth-first search agent.

    Since we can't clone environments, BFS is implemented by:
    1. Building a frontier of (action_path, state_hash) pairs.
    2. To explore a frontier node, undo back to root, then replay its action path.
    3. Try each untried action from that state, record new states.

    This is expensive in steps but guarantees finding the shortest solution.

    Config:
        max_depth: Maximum BFS depth.
        max_steps: Total step budget.
        max_frontier: Maximum frontier size before pruning.
    """

    def __init__(
        self,
        max_depth: int = 20,
        max_steps: int = 2000,
        max_frontier: int = 500,
    ):
        super().__init__("BFSAgent")
        self.max_depth = max_depth
        self.max_steps = max_steps
        self.max_frontier = max_frontier

        self.visited: set[str] = set()
        self.frontier: deque[BFSNode] = deque()
        self.current_target: BFSNode | None = None
        self.replay_index: int = 0
        self.phase: str = "init"  # init, undo, replay, explore
        self.undo_remaining: int = 0
        self.current_depth: int = 0
        self.step_count: int = 0
        self.explore_actions: list[GameAction] = []
        self.explore_index: int = 0

    def reset(self) -> None:
        self.visited.clear()
        self.frontier.clear()
        self.current_target = None
        self.replay_index = 0
        self.phase = "init"
        self.undo_remaining = 0
        self.current_depth = 0
        self.step_count = 0
        self.explore_actions.clear()
        self.explore_index = 0

    def choose_action(
        self, frames: list[FrameData], latest_frame: FrameData
    ) -> ActionWithData:
        self.step_count += 1
        state_hash = _hash_frame(latest_frame)

        # Phase: init — seed the frontier with root state
        if self.phase == "init":
            self.visited.add(state_hash)
            root = BFSNode(state_hash=state_hash, action_path=[], depth=0)
            # Add children of root to frontier
            for action in SIMPLE_ACTIONS:
                child = BFSNode(
                    state_hash="",  # unknown until explored
                    action_path=[action],
                    depth=1,
                )
                self.frontier.append(child)
            self.phase = "pick_next"
            # Explore the first action directly
            return self._pick_and_start_explore(latest_frame)

        # Phase: undo — backtrack to root
        if self.phase == "undo":
            if self.undo_remaining > 0:
                self.undo_remaining -= 1
                self.current_depth = max(0, self.current_depth - 1)
                return self.make_action(GameAction.ACTION7, reasoning="BFS undo to root")
            # Done undoing — start replaying target path
            self.phase = "replay"
            self.replay_index = 0
            if self.current_target and self.current_target.action_path:
                return self._replay_next()
            else:
                self.phase = "pick_next"
                return self._pick_and_start_explore(latest_frame)

        # Phase: replay — replay action path to reach target node's parent
        if self.phase == "replay":
            if self.current_target and self.replay_index < len(self.current_target.action_path) - 1:
                return self._replay_next()
            # Arrived at parent — now take the final action to explore
            if self.current_target and self.current_target.action_path:
                self.phase = "observe"
                action = self.current_target.action_path[-1]
                self.current_depth += 1
                return self.make_action(
                    action,
                    reasoning=f"BFS explore depth={self.current_target.depth}",
                )
            self.phase = "pick_next"
            return self._pick_and_start_explore(latest_frame)

        # Phase: observe — we just took the explore action, now observe result
        if self.phase == "observe":
            if state_hash not in self.visited:
                self.visited.add(state_hash)
                # Add children to frontier if within depth limit
                if self.current_target and self.current_target.depth < self.max_depth:
                    for action in SIMPLE_ACTIONS:
                        if len(self.frontier) < self.max_frontier:
                            child = BFSNode(
                                state_hash="",
                                action_path=self.current_target.action_path + [action],
                                depth=self.current_target.depth + 1,
                            )
                            self.frontier.append(child)
            self.phase = "pick_next"
            return self._pick_and_start_explore(latest_frame)

        # Phase: pick_next — select next frontier node
        if self.phase == "pick_next":
            return self._pick_and_start_explore(latest_frame)

        # Fallback
        return self.make_action(SIMPLE_ACTIONS[0], reasoning="BFS fallback")

    def _pick_and_start_explore(self, latest_frame: FrameData) -> ActionWithData:
        """Pick the next frontier node and begin navigating to it."""
        if not self.frontier:
            # Exhausted frontier — fall back to cycling actions
            action = SIMPLE_ACTIONS[self.step_count % len(SIMPLE_ACTIONS)]
            return self.make_action(action, reasoning="BFS frontier exhausted")

        self.current_target = self.frontier.popleft()

        # Undo to root first
        if self.current_depth > 0:
            self.undo_remaining = self.current_depth - 1  # -1 because we undo one now
            self.current_depth -= 1
            self.phase = "undo"
            return self.make_action(GameAction.ACTION7, reasoning="BFS undo to root")
        else:
            # Already at root — replay directly
            self.phase = "replay"
            self.replay_index = 0
            if len(self.current_target.action_path) > 1:
                return self._replay_next()
            elif self.current_target.action_path:
                # Single action from root
                self.phase = "observe"
                action = self.current_target.action_path[0]
                self.current_depth = 1
                return self.make_action(
                    action,
                    reasoning=f"BFS explore depth={self.current_target.depth}",
                )
            else:
                self.phase = "pick_next"
                return self._pick_and_start_explore(latest_frame)

    def _replay_next(self) -> ActionWithData:
        """Replay the next action in the path to reach the target."""
        action = self.current_target.action_path[self.replay_index]
        self.replay_index += 1
        self.current_depth += 1
        return self.make_action(action, reasoning=f"BFS replay step {self.replay_index}")

    def is_done(self, frames: list[FrameData], latest_frame: FrameData) -> bool:
        if latest_frame.state == GameState.WIN:
            return True
        if latest_frame.is_terminal:
            return True
        if self.step_count >= self.max_steps:
            return True
        if not self.frontier and self.phase == "pick_next":
            return True
        return False
