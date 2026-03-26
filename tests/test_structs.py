"""Tests for agent data structures."""

from agents.structs import (
    ActionWithData,
    FrameData,
    GameAction,
    GameState,
    SIMPLE_ACTIONS,
)


def test_game_action_values():
    assert GameAction.RESET == 0
    assert GameAction.ACTION1 == 1
    assert GameAction.ACTION7 == 7


def test_game_action_with_data():
    awd = GameAction.ACTION6.with_data(x=10, y=20)
    assert awd.action == GameAction.ACTION6
    assert awd.data == {"x": 10, "y": 20}


def test_simple_actions():
    assert len(SIMPLE_ACTIONS) == 5
    assert GameAction.RESET not in SIMPLE_ACTIONS
    assert GameAction.ACTION7 not in SIMPLE_ACTIONS


def test_frame_data_terminal_states():
    assert FrameData(state=GameState.WIN).is_terminal is True
    assert FrameData(state=GameState.LOSE).is_terminal is True
    assert FrameData(state=GameState.TIMEOUT).is_terminal is True
    assert FrameData(state=GameState.RUNNING).is_terminal is False


def test_frame_data_is_win():
    assert FrameData(state=GameState.WIN).is_win is True
    assert FrameData(state=GameState.RUNNING).is_win is False


def test_action_with_data_set_data():
    awd = ActionWithData(action=GameAction.ACTION6)
    awd.set_data({"x": 5, "y": 10})
    assert awd.data == {"x": 5, "y": 10}
