"""A* search agent for ARC-AGI-3.

Combines DFS-style depth exploration with heuristic-guided priority.
Uses the StateEvaluator to score states and explore the most promising
branches first, while still using undo for backtracking.
"""

from __future__ import annotations

import hashlib
import heapq
from dataclasses import dataclass, field

from .agent import Agent
from .heuristics import ActionPrioritizer, StateEvaluator
from .structs import ActionWithData, FrameData, GameAction, GameState, SIMPLE_ACTIONS


def _hash_frame(frame: FrameData) -> str:
    if frame.grid is not None:
        content = str(frame.grid)
    else:
        content = frame.render
    content += f"|lv={frame.levels_completed}"
    return hashlib.md5(content.encode(), usedforsecurity=False).hexdigest()[:16]


@dataclass(order=True)
class PriorityNode:
    """Node in the priority queue, ordered by negative score (higher = better)."""

    neg_score: float
    action_path: list[GameAction] = field(compare=False)
    state_hash: str = field(compare=False)
    depth: int = field(compare=False)


class AStarAgent(Agent):
    """A* search agent guided by state evaluation heuristics.

    Uses a priority queue instead of a stack (DFS) or queue (BFS).
    States are scored by the StateEvaluator, and the most promising
    states are explored first.

    Navigation works the same as BFS: undo to root, replay path, explore.

    Config:
        max_depth: Maximum search depth.
        max_steps: Total step budget.
        max_queue: Maximum priority queue size.
    """

    def __init__(
        self,
        max_depth: int = 30,
        max_steps: int = 1500,
        max_queue: int = 300,
    ):
        super().__init__("AStarAgent")
        self.max_depth = max_depth
        self.max_steps = max_steps
        self.max_queue = max_queue

        self.evaluator = StateEvaluator()
        self.prioritizer = ActionPrioritizer()
        self.visited: set[str] = set()
        self.pq: list[PriorityNode] = []  # min-heap (neg scores)
        self.current_target: PriorityNode | None = None
        self.current_depth: int = 0
        self.step_count: int = 0
        self.phase: str = "init"
        self.undo_remaining: int = 0
        self.replay_index: int = 0
        self.prev_frame: FrameData | None = None

    def reset(self) -> None:
        self.evaluator.reset()
        self.prioritizer.reset()
        self.visited.clear()
        self.pq.clear()
        self.current_target = None
        self.current_depth = 0
        self.step_count = 0
        self.phase = "init"
        self.undo_remaining = 0
        self.replay_index = 0
        self.prev_frame = None

    def _add_children(self, parent_path: list[GameAction], depth: int, score: float):
        """Add child nodes to the priority queue."""
        actions = self.prioritizer.prioritize(list(SIMPLE_ACTIONS))
        for i, action in enumerate(actions):
            if len(self.pq) >= self.max_queue:
                break
            # Slight bonus for prioritized actions
            child_score = score + 0.1 * (len(actions) - i) / len(actions)
            node = PriorityNode(
                neg_score=-child_score,
                action_path=parent_path + [action],
                state_hash="",
                depth=depth + 1,
            )
            heapq.heappush(self.pq, node)

    def choose_action(
        self, frames: list[FrameData], latest_frame: FrameData
    ) -> ActionWithData:
        self.step_count += 1
        state_hash = _hash_frame(latest_frame)

        if self.phase == "init":
            self.visited.add(state_hash)
            score = self.evaluator.evaluate(latest_frame).combined
            self._add_children([], 0, score)
            self.phase = "pick_next"
            return self._pick_and_navigate(latest_frame)

        if self.phase == "undo":
            if self.undo_remaining > 0:
                self.undo_remaining -= 1
                self.current_depth = max(0, self.current_depth - 1)
                return self.make_action(GameAction.ACTION7, reasoning="A* undo")
            self.phase = "replay"
            self.replay_index = 0
            if self.current_target and len(self.current_target.action_path) > 1:
                return self._replay_next()
            elif self.current_target and self.current_target.action_path:
                self.phase = "observe"
                action = self.current_target.action_path[0]
                self.current_depth = 1
                return self.make_action(action, reasoning=f"A* explore d={self.current_target.depth}")
            return self._pick_and_navigate(latest_frame)

        if self.phase == "replay":
            if self.current_target and self.replay_index < len(self.current_target.action_path) - 1:
                return self._replay_next()
            if self.current_target and self.current_target.action_path:
                self.phase = "observe"
                action = self.current_target.action_path[-1]
                self.current_depth += 1
                return self.make_action(action, reasoning=f"A* explore d={self.current_target.depth}")
            return self._pick_and_navigate(latest_frame)

        if self.phase == "observe":
            state_score = self.evaluator.evaluate(latest_frame, self.prev_frame)

            # Record action effectiveness
            if self.current_target and self.current_target.action_path:
                last_action = self.current_target.action_path[-1]
                self.prioritizer.record(last_action, state_score)

            if state_hash not in self.visited:
                self.visited.add(state_hash)
                if self.current_target and self.current_target.depth < self.max_depth:
                    self._add_children(
                        self.current_target.action_path,
                        self.current_target.depth,
                        state_score.combined,
                    )

            self.prev_frame = latest_frame
            self.phase = "pick_next"
            return self._pick_and_navigate(latest_frame)

        if self.phase == "pick_next":
            return self._pick_and_navigate(latest_frame)

        return self.make_action(SIMPLE_ACTIONS[0], reasoning="A* fallback")

    def _pick_and_navigate(self, latest_frame: FrameData) -> ActionWithData:
        if not self.pq:
            action = SIMPLE_ACTIONS[self.step_count % len(SIMPLE_ACTIONS)]
            return self.make_action(action, reasoning="A* queue exhausted")

        self.current_target = heapq.heappop(self.pq)

        if self.current_depth > 0:
            self.undo_remaining = self.current_depth - 1
            self.current_depth -= 1
            self.phase = "undo"
            return self.make_action(GameAction.ACTION7, reasoning="A* undo to root")
        else:
            self.phase = "replay"
            self.replay_index = 0
            if len(self.current_target.action_path) > 1:
                return self._replay_next()
            elif self.current_target.action_path:
                self.phase = "observe"
                action = self.current_target.action_path[0]
                self.current_depth = 1
                return self.make_action(action, reasoning=f"A* explore d={self.current_target.depth}")
            return self._pick_and_navigate(latest_frame)

    def _replay_next(self) -> ActionWithData:
        action = self.current_target.action_path[self.replay_index]
        self.replay_index += 1
        self.current_depth += 1
        return self.make_action(action, reasoning=f"A* replay {self.replay_index}")

    def is_done(self, frames: list[FrameData], latest_frame: FrameData) -> bool:
        if latest_frame.state == GameState.WIN:
            return True
        if latest_frame.is_terminal:
            return True
        if self.step_count >= self.max_steps:
            return True
        return False
