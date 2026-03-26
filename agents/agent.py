"""Base agent class for ARC-AGI-3."""

from __future__ import annotations

from abc import ABC, abstractmethod

from .structs import ActionWithData, FrameData, GameAction


class Agent(ABC):
    """Abstract base class for all ARC-AGI-3 agents.

    Subclasses must implement:
        - choose_action(): decide what to do given observation history
        - is_done(): determine if the agent considers the game finished
    """

    def __init__(self, name: str | None = None):
        self.name = name or self.__class__.__name__

    @abstractmethod
    def choose_action(
        self, frames: list[FrameData], latest_frame: FrameData
    ) -> ActionWithData:
        """Select the next action based on observation history.

        Args:
            frames: Full history of observations so far.
            latest_frame: The most recent observation.

        Returns:
            An ActionWithData containing the chosen action and optional data/reasoning.
        """
        ...

    @abstractmethod
    def is_done(self, frames: list[FrameData], latest_frame: FrameData) -> bool:
        """Determine whether the agent considers the game finished.

        Args:
            frames: Full history of observations.
            latest_frame: The most recent observation.

        Returns:
            True if the agent wants to stop playing.
        """
        ...

    def reset(self) -> None:
        """Reset internal state for a new game. Override if needed."""
        pass

    def make_action(
        self, action: GameAction, reasoning: str = "", **data
    ) -> ActionWithData:
        """Helper to construct an ActionWithData."""
        awd = ActionWithData(action=action, reasoning=reasoning)
        if data:
            awd.set_data(data)
        return awd
