"""Data structures for ARC-AGI-3 agent interaction."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, IntEnum


class GameState(Enum):
    """Possible states of a game environment."""

    RUNNING = "running"
    WIN = "win"
    LOSE = "lose"
    TIMEOUT = "timeout"


class GameAction(IntEnum):
    """Actions available in ARC-AGI-3 environments.

    Actions 1-5: directional/simple actions
    Action 6: coordinate-based action (requires x, y data)
    Action 7: undo
    """

    RESET = 0
    ACTION1 = 1  # Up
    ACTION2 = 2  # Down
    ACTION3 = 3  # Left
    ACTION4 = 4  # Right
    ACTION5 = 5  # Interact / Select / Rotate / Execute
    ACTION6 = 6  # Coordinate-based (needs x, y in 0-63)
    ACTION7 = 7  # Undo

    def with_data(self, x: int, y: int) -> ActionWithData:
        """Create an action with coordinate data (for ACTION6)."""
        return ActionWithData(action=self, data={"x": x, "y": y})


# All simple (non-coordinate) actions for search/exploration
SIMPLE_ACTIONS = [
    GameAction.ACTION1,
    GameAction.ACTION2,
    GameAction.ACTION3,
    GameAction.ACTION4,
    GameAction.ACTION5,
]


@dataclass
class ActionWithData:
    """An action bundled with optional coordinate data and reasoning."""

    action: GameAction
    data: dict | None = None
    reasoning: str = ""

    def set_data(self, data: dict) -> None:
        self.data = data


@dataclass
class FrameData:
    """Observation data returned after each environment step."""

    frame_number: int = 0
    state: GameState = GameState.RUNNING
    levels_completed: int = 0
    win_levels: int = 1
    available_actions: list[GameAction] = field(default_factory=list)
    grid: list[list[int]] | None = None
    render: str = ""
    metadata: dict = field(default_factory=dict)

    @property
    def is_terminal(self) -> bool:
        return self.state in (GameState.WIN, GameState.LOSE, GameState.TIMEOUT)

    @property
    def is_win(self) -> bool:
        return self.state == GameState.WIN
