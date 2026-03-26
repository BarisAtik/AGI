"""Depth-First Search agent for ARC-AGI-3.

Strategy:
  Treats each game as a search problem. Explores action sequences depth-first,
  using undo (ACTION7) to backtrack when a branch looks unpromising. Tracks
  visited states via grid hashes to avoid cycles.

  This is a baseline systematic explorer — nightshift tasks will iteratively
  improve heuristics, pruning, and state evaluation over time.
"""

from __future__ import annotations

import hashlib
from collections import deque
from dataclasses import dataclass, field

from .agent import Agent
from .structs import ActionWithData, FrameData, GameAction, GameState, SIMPLE_ACTIONS


def _hash_frame(frame: FrameData) -> str:
    """Create a compact hash of the observable state for cycle detection."""
    # Use grid if available, otherwise fall back to render string
    if frame.grid is not None:
        content = str(frame.grid)
    else:
        content = frame.render
    content += f"|lv={frame.levels_completed}"
    return hashlib.md5(content.encode(), usedforsecurity=False).hexdigest()[:16]


@dataclass
class SearchNode:
    """A node in the DFS search tree."""

    state_hash: str
    action_taken: GameAction | None  # action that led here
    depth: int
    children_tried: list[GameAction] = field(default_factory=list)


class DFSAgent(Agent):
    """Depth-first search agent that systematically explores the action space.

    The agent maintains a search stack. At each step it:
    1. Checks if the current state is new (not visited).
    2. If new, picks the next untried action from the available set.
    3. If all actions tried or state already visited, backtracks via ACTION7.
    4. Continues until it wins or exhausts the search budget.

    Config:
        max_depth: Maximum search depth before forced backtrack.
        max_steps: Total step budget for the episode.
        prefer_actions: Ordered list of actions to try first (heuristic priority).
    """

    def __init__(
        self,
        max_depth: int = 50,
        max_steps: int = 1000,
        prefer_actions: list[GameAction] | None = None,
    ):
        super().__init__("DFSAgent")
        self.max_depth = max_depth
        self.max_steps = max_steps
        self.prefer_actions = prefer_actions or list(SIMPLE_ACTIONS)

        # Search state
        self.visited: set[str] = set()
        self.stack: list[SearchNode] = []
        self.backtracking = False
        self.backtrack_count = 0
        self.step_count = 0

    def reset(self) -> None:
        self.visited.clear()
        self.stack.clear()
        self.backtracking = False
        self.backtrack_count = 0
        self.step_count = 0

    def _get_action_order(self, available: list[GameAction]) -> list[GameAction]:
        """Return actions in preferred exploration order, filtered by availability."""
        available_set = set(available) if available else set(self.prefer_actions)
        ordered = []
        for a in self.prefer_actions:
            if a in available_set:
                ordered.append(a)
        # Add any available actions not in our preference list
        for a in available:
            if a not in ordered and a not in (GameAction.RESET, GameAction.ACTION7):
                ordered.append(a)
        return ordered

    def choose_action(
        self, frames: list[FrameData], latest_frame: FrameData
    ) -> ActionWithData:
        self.step_count += 1
        state_hash = _hash_frame(latest_frame)

        # If we're backtracking, keep undoing until we reach an unexplored branch
        if self.backtracking:
            if self.stack:
                current_node = self.stack[-1]
                action_order = self._get_action_order(latest_frame.available_actions)
                untried = [a for a in action_order if a not in current_node.children_tried]

                if untried:
                    # Found an untried branch at this depth — stop backtracking
                    self.backtracking = False
                    next_action = untried[0]
                    current_node.children_tried.append(next_action)
                    self.stack.append(
                        SearchNode(
                            state_hash=state_hash,
                            action_taken=next_action,
                            depth=current_node.depth + 1,
                        )
                    )
                    return self.make_action(
                        next_action,
                        reasoning=f"DFS explore (depth={current_node.depth + 1}, "
                        f"backtracked {self.backtrack_count}x)",
                    )
                else:
                    # All branches tried at this level, keep backtracking
                    self.stack.pop()
                    self.backtrack_count += 1
                    return self.make_action(GameAction.ACTION7, reasoning="DFS backtrack (undo)")
            else:
                # Stack empty — exhausted search from root; try random fallback
                self.backtracking = False
                action = self.prefer_actions[self.step_count % len(self.prefer_actions)]
                return self.make_action(action, reasoning="DFS exhausted, cycling actions")

        # Normal forward exploration
        is_new_state = state_hash not in self.visited
        self.visited.add(state_hash)

        current_depth = self.stack[-1].depth if self.stack else 0

        # Check if we should backtrack (depth limit or revisited state)
        if current_depth >= self.max_depth or (not is_new_state and self.stack):
            self.backtracking = True
            self.backtrack_count += 1
            if self.stack:
                self.stack.pop()
            return self.make_action(
                GameAction.ACTION7,
                reasoning=f"DFS backtrack: {'depth limit' if current_depth >= self.max_depth else 'revisited state'}",
            )

        # Pick next untried action
        action_order = self._get_action_order(latest_frame.available_actions)

        if self.stack:
            current_node = self.stack[-1]
            untried = [a for a in action_order if a not in current_node.children_tried]
        else:
            untried = action_order

        if not untried:
            # All actions tried at this node — backtrack
            self.backtracking = True
            self.backtrack_count += 1
            if self.stack:
                self.stack.pop()
            return self.make_action(GameAction.ACTION7, reasoning="DFS backtrack: all tried")

        next_action = untried[0]

        # Record which action we're trying
        if self.stack:
            self.stack[-1].children_tried.append(next_action)

        # Push new node
        self.stack.append(
            SearchNode(
                state_hash=state_hash,
                action_taken=next_action,
                depth=current_depth + 1,
            )
        )

        return self.make_action(
            next_action,
            reasoning=f"DFS explore (depth={current_depth + 1}, visited={len(self.visited)})",
        )

    def is_done(self, frames: list[FrameData], latest_frame: FrameData) -> bool:
        if latest_frame.state == GameState.WIN:
            return True
        if latest_frame.is_terminal:
            return True
        if self.step_count >= self.max_steps:
            return True
        return False
