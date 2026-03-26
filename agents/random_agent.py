"""Random baseline agent for ARC-AGI-3."""

from __future__ import annotations

import random

from .agent import Agent
from .structs import ActionWithData, FrameData, GameAction, GameState, SIMPLE_ACTIONS


class RandomAgent(Agent):
    """Baseline agent that selects random actions from the available action space."""

    def __init__(self, max_steps: int = 500):
        super().__init__("RandomAgent")
        self.max_steps = max_steps

    def choose_action(
        self, frames: list[FrameData], latest_frame: FrameData
    ) -> ActionWithData:
        if latest_frame.available_actions:
            action = random.choice(latest_frame.available_actions)
        else:
            action = random.choice(SIMPLE_ACTIONS)
        return self.make_action(action, reasoning="random exploration")

    def is_done(self, frames: list[FrameData], latest_frame: FrameData) -> bool:
        if latest_frame.state == GameState.WIN:
            return True
        if len(frames) >= self.max_steps:
            return True
        return latest_frame.is_terminal
