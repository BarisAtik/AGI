"""Tests for the A* agent."""

from agents.structs import FrameData, GameAction, GameState, SIMPLE_ACTIONS
from agents.astar_agent import AStarAgent


def test_astar_agent_init():
    agent = AStarAgent(max_depth=15, max_steps=300)
    assert agent.name == "AStarAgent"
    assert agent.max_depth == 15
    assert agent.max_steps == 300


def test_astar_agent_reset():
    agent = AStarAgent()
    agent.visited.add("state1")
    agent.step_count = 100
    agent.reset()
    assert len(agent.visited) == 0
    assert agent.step_count == 0
    assert len(agent.pq) == 0


def test_astar_agent_chooses_action():
    agent = AStarAgent(max_depth=5, max_steps=50)
    frame = FrameData(frame_number=0, available_actions=list(SIMPLE_ACTIONS))
    frames = [frame]
    action = agent.choose_action(frames, frame)
    assert action.action in list(SIMPLE_ACTIONS) + [GameAction.ACTION7]


def test_astar_agent_terminates_on_win():
    agent = AStarAgent()
    frame = FrameData(frame_number=1, state=GameState.WIN)
    assert agent.is_done([frame], frame) is True


def test_astar_agent_terminates_on_max_steps():
    agent = AStarAgent(max_steps=10)
    agent.step_count = 10
    frame = FrameData(frame_number=10)
    assert agent.is_done([frame], frame) is True


def test_astar_agent_uses_heuristics():
    agent = AStarAgent(max_depth=5, max_steps=50)
    frame = FrameData(
        frame_number=0,
        available_actions=list(SIMPLE_ACTIONS),
        levels_completed=0,
        win_levels=3,
    )
    frames = [frame]

    # Run a few steps
    for _ in range(10):
        if agent.is_done(frames, frame):
            break
        agent.choose_action(frames, frame)

    # Evaluator should have recorded some states
    assert len(agent.evaluator.seen_hashes) > 0
