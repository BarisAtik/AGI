from .agent import Agent
from .structs import FrameData, GameAction, GameState
from .random_agent import RandomAgent
from .dfs_agent import DFSAgent
from .bfs_agent import BFSAgent
from .astar_agent import AStarAgent
from .heuristics import StateEvaluator, ActionPrioritizer

AVAILABLE_AGENTS = {
    "random": RandomAgent,
    "dfs": DFSAgent,
    "bfs": BFSAgent,
    "astar": AStarAgent,
}

__all__ = [
    "Agent",
    "FrameData",
    "GameAction",
    "GameState",
    "RandomAgent",
    "DFSAgent",
    "BFSAgent",
    "AStarAgent",
    "StateEvaluator",
    "ActionPrioritizer",
    "AVAILABLE_AGENTS",
]
