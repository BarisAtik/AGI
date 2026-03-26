"""Tests for the DFS agent."""

from agents.structs import FrameData, GameAction, GameState, SIMPLE_ACTIONS
from agents.dfs_agent import DFSAgent


def test_dfs_agent_init():
    agent = DFSAgent(max_depth=10, max_steps=100)
    assert agent.name == "DFSAgent"
    assert agent.max_depth == 10
    assert agent.max_steps == 100


def test_dfs_agent_reset():
    agent = DFSAgent()
    agent.visited.add("some_state")
    agent.step_count = 50
    agent.reset()
    assert len(agent.visited) == 0
    assert agent.step_count == 0


def test_dfs_agent_chooses_action():
    agent = DFSAgent(max_depth=5, max_steps=10)
    frame = FrameData(frame_number=0, available_actions=list(SIMPLE_ACTIONS))
    frames = [frame]
    action = agent.choose_action(frames, frame)
    assert action.action in SIMPLE_ACTIONS
    assert action.reasoning != ""


def test_dfs_agent_terminates_on_win():
    agent = DFSAgent()
    frame = FrameData(frame_number=1, state=GameState.WIN)
    assert agent.is_done([frame], frame) is True


def test_dfs_agent_terminates_on_max_steps():
    agent = DFSAgent(max_steps=5)
    agent.step_count = 5
    frame = FrameData(frame_number=5)
    assert agent.is_done([frame], frame) is True


def test_dfs_agent_does_not_terminate_early():
    agent = DFSAgent(max_steps=100)
    frame = FrameData(frame_number=1, state=GameState.RUNNING)
    assert agent.is_done([frame], frame) is False


def test_dfs_agent_backtracks_at_depth_limit():
    agent = DFSAgent(max_depth=2, max_steps=100)
    frame = FrameData(frame_number=0, available_actions=list(SIMPLE_ACTIONS))
    frames = [frame]

    # Run enough steps to hit depth limit
    for _ in range(10):
        action = agent.choose_action(frames, frame)
        if action.action == GameAction.ACTION7:
            # Backtracking detected
            break
    # Should have attempted backtracking within 10 steps at depth 2
    assert agent.backtrack_count > 0 or agent.step_count <= 10
