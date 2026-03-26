"""State evaluation heuristics for search-based agents.

Provides scoring functions that help agents prioritize which states
to explore and when to prune branches. These heuristics are the main
lever for improving search efficiency — nightshift will iteratively
improve them.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from .structs import FrameData, GameAction


@dataclass
class StateScore:
    """Composite score for a game state."""

    progress: float = 0.0  # 0-1, how close to winning
    novelty: float = 0.0   # 0-1, how different from seen states
    activity: float = 0.0  # 0-1, how much changed from last frame
    combined: float = 0.0  # weighted combination


class StateEvaluator:
    """Evaluates game states to guide search.

    The evaluator maintains history to compute novelty and change detection.
    All heuristics return normalized 0-1 scores.
    """

    def __init__(
        self,
        progress_weight: float = 0.5,
        novelty_weight: float = 0.3,
        activity_weight: float = 0.2,
    ):
        self.progress_weight = progress_weight
        self.novelty_weight = novelty_weight
        self.activity_weight = activity_weight

        self.seen_hashes: set[str] = set()
        self.grid_history: list[list[list[int]]] = []

    def reset(self) -> None:
        self.seen_hashes.clear()
        self.grid_history.clear()

    def _hash_grid(self, grid: list[list[int]] | None) -> str:
        if grid is None:
            return "none"
        return hashlib.md5(str(grid).encode(), usedforsecurity=False).hexdigest()[:16]

    def progress_score(self, frame: FrameData) -> float:
        """Score based on level completion progress."""
        if frame.win_levels == 0:
            return 0.0
        return frame.levels_completed / frame.win_levels

    def novelty_score(self, frame: FrameData) -> float:
        """Score based on how novel this state is (unseen = 1.0, seen = 0.0)."""
        h = self._hash_grid(frame.grid)
        if h in self.seen_hashes:
            return 0.0
        self.seen_hashes.add(h)
        return 1.0

    def activity_score(self, frame: FrameData, prev_frame: FrameData | None) -> float:
        """Score based on how much the grid changed from the previous frame."""
        if frame.grid is None or prev_frame is None or prev_frame.grid is None:
            return 0.5  # uncertain, return middle score

        if len(frame.grid) != len(prev_frame.grid):
            return 1.0  # grid size changed — high activity

        changed = 0
        total = 0
        for r1, r2 in zip(frame.grid, prev_frame.grid):
            for c1, c2 in zip(r1, r2):
                total += 1
                if c1 != c2:
                    changed += 1

        if total == 0:
            return 0.0
        return changed / total

    def evaluate(
        self, frame: FrameData, prev_frame: FrameData | None = None
    ) -> StateScore:
        """Compute a composite score for the given state."""
        progress = self.progress_score(frame)
        novelty = self.novelty_score(frame)
        activity = self.activity_score(frame, prev_frame)

        combined = (
            self.progress_weight * progress
            + self.novelty_weight * novelty
            + self.activity_weight * activity
        )

        if frame.grid is not None:
            self.grid_history.append(frame.grid)

        return StateScore(
            progress=progress,
            novelty=novelty,
            activity=activity,
            combined=combined,
        )

    def should_prune(self, frame: FrameData, threshold: float = 0.05) -> bool:
        """Suggest whether a branch should be pruned.

        Prunes if: state is not novel AND no progress AND low activity.
        """
        score = self.evaluate(frame)
        return score.combined < threshold and score.novelty == 0.0


class ActionPrioritizer:
    """Reorders actions based on historical effectiveness.

    Tracks which actions led to progress or novel states and prioritizes
    them in future exploration.
    """

    def __init__(self):
        self.action_scores: dict[GameAction, float] = {}
        self.action_counts: dict[GameAction, int] = {}

    def reset(self) -> None:
        self.action_scores.clear()
        self.action_counts.clear()

    def record(self, action: GameAction, state_score: StateScore) -> None:
        """Record the outcome of taking an action."""
        count = self.action_counts.get(action, 0) + 1
        self.action_counts[action] = count

        prev = self.action_scores.get(action, 0.0)
        # Running average
        self.action_scores[action] = prev + (state_score.combined - prev) / count

    def prioritize(self, actions: list[GameAction]) -> list[GameAction]:
        """Sort actions by historical effectiveness (best first)."""
        return sorted(
            actions,
            key=lambda a: self.action_scores.get(a, 0.5),
            reverse=True,
        )
