"""Tests for state evaluation heuristics."""

from agents.structs import FrameData, GameAction, GameState
from agents.heuristics import StateEvaluator, ActionPrioritizer, StateScore


def test_evaluator_progress_score():
    ev = StateEvaluator()
    frame = FrameData(levels_completed=2, win_levels=4)
    assert ev.progress_score(frame) == 0.5

    frame_win = FrameData(levels_completed=4, win_levels=4)
    assert ev.progress_score(frame_win) == 1.0

    frame_zero = FrameData(levels_completed=0, win_levels=0)
    assert ev.progress_score(frame_zero) == 0.0


def test_evaluator_novelty_score():
    ev = StateEvaluator()
    frame = FrameData(grid=[[1, 2], [3, 4]])

    # First time seeing this state
    assert ev.novelty_score(frame) == 1.0
    # Second time — not novel
    assert ev.novelty_score(frame) == 0.0


def test_evaluator_activity_score():
    ev = StateEvaluator()
    f1 = FrameData(grid=[[0, 0], [0, 0]])
    f2 = FrameData(grid=[[1, 0], [0, 0]])

    score = ev.activity_score(f2, f1)
    assert score == 0.25  # 1 out of 4 cells changed


def test_evaluator_activity_no_grid():
    ev = StateEvaluator()
    f1 = FrameData(grid=None)
    f2 = FrameData(grid=None)
    assert ev.activity_score(f2, f1) == 0.5  # uncertain


def test_evaluator_combined_score():
    ev = StateEvaluator()
    frame = FrameData(grid=[[1, 2]], levels_completed=1, win_levels=2)
    score = ev.evaluate(frame)
    assert isinstance(score, StateScore)
    assert 0 <= score.combined <= 1.0
    assert score.progress == 0.5
    assert score.novelty == 1.0  # first time


def test_evaluator_should_prune():
    ev = StateEvaluator(progress_weight=0.5, novelty_weight=0.3, activity_weight=0.2)
    frame = FrameData(grid=[[0, 0]], levels_completed=0, win_levels=5)

    # First visit — novel, should not prune
    assert ev.should_prune(frame) is False

    # should_prune calls evaluate internally, which uses default prev_frame=None
    # giving activity=0.5. With novelty=0 and progress=0:
    # combined = 0.5*0 + 0.3*0 + 0.2*0.5 = 0.1, above default 0.05 threshold
    # Use a stricter threshold to test pruning of revisited zero-progress states
    assert ev.should_prune(frame, threshold=0.15) is True


def test_action_prioritizer():
    p = ActionPrioritizer()
    good_score = StateScore(combined=0.9)
    bad_score = StateScore(combined=0.1)

    p.record(GameAction.ACTION1, good_score)
    p.record(GameAction.ACTION2, bad_score)
    p.record(GameAction.ACTION3, good_score)

    ordered = p.prioritize([GameAction.ACTION1, GameAction.ACTION2, GameAction.ACTION3])
    # ACTION1 and ACTION3 should come before ACTION2
    assert ordered[-1] == GameAction.ACTION2


def test_action_prioritizer_reset():
    p = ActionPrioritizer()
    p.record(GameAction.ACTION1, StateScore(combined=0.5))
    p.reset()
    assert len(p.action_scores) == 0
