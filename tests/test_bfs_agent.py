"""Tests for the BFS agent."""

from agents.structs import FrameData, GameAction, GameState, SIMPLE_ACTIONS
from agents.bfs_agent import BFSAgent


def test_bfs_agent_init():
    agent = BFSAgent(max_depth=10, max_steps=200)
    assert agent.name == "BFSAgent"
    assert agent.max_depth == 10
    assert agent.max_steps == 200


def test_bfs_agent_reset():
    agent = BFSAgent()
    agent.visited.add("state1")
    agent.step_count = 50
    agent.reset()
    assert len(agent.visited) == 0
    assert agent.step_count == 0
    assert agent.phase == "init"


def test_bfs_agent_chooses_action():
    agent = BFSAgent(max_depth=5, max_steps=50)
    frame = FrameData(frame_number=0, available_actions=list(SIMPLE_ACTIONS))
    frames = [frame]
    action = agent.choose_action(frames, frame)
    assert action.action in list(SIMPLE_ACTIONS) + [GameAction.ACTION7]
    assert action.reasoning != ""


def test_bfs_agent_terminates_on_win():
    agent = BFSAgent()
    frame = FrameData(frame_number=1, state=GameState.WIN)
    assert agent.is_done([frame], frame) is True


def test_bfs_agent_terminates_on_max_steps():
    agent = BFSAgent(max_steps=5)
    agent.step_count = 5
    frame = FrameData(frame_number=5)
    assert agent.is_done([frame], frame) is True


def test_bfs_agent_explores_breadth_first():
    agent = BFSAgent(max_depth=3, max_steps=30)
    frame = FrameData(frame_number=0, available_actions=list(SIMPLE_ACTIONS))
    frames = [frame]

    # Run several steps and verify it produces actions
    actions_seen = set()
    for _ in range(20):
        if agent.is_done(frames, frame):
            break
        action = agent.choose_action(frames, frame)
        actions_seen.add(action.action)

    # Should have tried multiple different actions (exploring breadth)
    assert len(actions_seen) >= 2
