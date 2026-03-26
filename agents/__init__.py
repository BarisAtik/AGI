from .agent import Agent
from .structs import FrameData, GameAction, GameState
from .random_agent import RandomAgent
from .dfs_agent import DFSAgent

AVAILABLE_AGENTS = {
    "random": RandomAgent,
    "dfs": DFSAgent,
}

__all__ = [
    "Agent",
    "FrameData",
    "GameAction",
    "GameState",
    "RandomAgent",
    "DFSAgent",
    "AVAILABLE_AGENTS",
]
