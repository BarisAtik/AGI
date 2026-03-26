#!/usr/bin/env python3
"""Kaggle submission pipeline for ARC Prize 2026 (ARC-AGI-3).

Generates a submission by running our agent against all competition games
and formatting results for Kaggle upload.

Usage:
    python kaggle/submit.py --agent=dfs --output=kaggle/submission/results.json
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def get_competition_games() -> list[str]:
    """Retrieve the list of competition game IDs.

    In the real competition, this will come from the Kaggle dataset
    or the ARC-AGI API. For now, returns a placeholder list.
    """
    try:
        from arc_agi import Arcade

        arc = Arcade()
        # The SDK should provide a way to list competition games
        games = arc.list_games() if hasattr(arc, "list_games") else []
        if games:
            return [g.id if hasattr(g, "id") else str(g) for g in games]
    except ImportError:
        pass

    # Placeholder — replace with actual competition game IDs
    return []


def run_agent_on_game(agent, game_id: str, max_steps: int = 1000) -> dict:
    """Run an agent on a single game and return the result."""
    from agents.structs import FrameData, GameAction, GameState

    agent.reset()
    frames: list[FrameData] = [FrameData(frame_number=0)]
    start = time.time()

    try:
        from arc_agi import Arcade
        from arc_agi.types import GameAction as SDKGameAction

        arc = Arcade()
        env = arc.make(game_id)

        sdk_map = {
            GameAction.RESET: SDKGameAction.RESET,
            GameAction.ACTION1: SDKGameAction.ACTION1,
            GameAction.ACTION2: SDKGameAction.ACTION2,
            GameAction.ACTION3: SDKGameAction.ACTION3,
            GameAction.ACTION4: SDKGameAction.ACTION4,
            GameAction.ACTION5: SDKGameAction.ACTION5,
            GameAction.ACTION6: SDKGameAction.ACTION6,
            GameAction.ACTION7: SDKGameAction.ACTION7,
        }

        step = 0
        while not agent.is_done(frames, frames[-1]):
            action = agent.choose_action(frames, frames[-1])
            sdk_action = sdk_map[action.action]

            if action.data:
                obs = env.step(sdk_action, data=action.data)
            else:
                obs = env.step(sdk_action)

            step += 1
            frame = FrameData(
                frame_number=step,
                state=GameState(obs.state.value) if hasattr(obs, "state") else GameState.RUNNING,
                levels_completed=getattr(obs, "levels_completed", 0),
                win_levels=getattr(obs, "win_levels", 1),
                grid=getattr(obs, "grid", None),
                render=getattr(obs, "render", ""),
            )
            frames.append(frame)

        scorecard = arc.get_scorecard()
        elapsed = time.time() - start

        return {
            "game_id": game_id,
            "status": "completed",
            "steps": step,
            "elapsed_seconds": round(elapsed, 2),
            "final_state": frames[-1].state.value,
            "levels_completed": frames[-1].levels_completed,
            "win_levels": frames[-1].win_levels,
            "scorecard": scorecard if isinstance(scorecard, dict) else str(scorecard),
        }

    except ImportError:
        return {
            "game_id": game_id,
            "status": "skipped",
            "reason": "arc-agi SDK not installed",
        }
    except Exception as e:
        return {
            "game_id": game_id,
            "status": "error",
            "error": str(e),
            "elapsed_seconds": round(time.time() - start, 2),
        }


def main():
    parser = argparse.ArgumentParser(description="ARC-AGI-3 Kaggle Submission Generator")
    parser.add_argument("--agent", default="dfs", choices=["random", "dfs"])
    parser.add_argument("--max-steps", type=int, default=1000)
    parser.add_argument("--max-depth", type=int, default=50)
    parser.add_argument("--output", default="kaggle/submission/results.json")
    parser.add_argument("--games", nargs="*", help="Specific game IDs to run (default: all)")
    args = parser.parse_args()

    from agents import AVAILABLE_AGENTS

    agent_cls = AVAILABLE_AGENTS[args.agent]
    if args.agent == "dfs":
        agent = agent_cls(max_depth=args.max_depth, max_steps=args.max_steps)
    else:
        agent = agent_cls(max_steps=args.max_steps)

    games = args.games or get_competition_games()

    if not games:
        print("No games found. Provide game IDs via --games or install arc-agi SDK.")
        print("Example: python kaggle/submit.py --agent=dfs --games ls20 ft09")
        sys.exit(1)

    print(f"Running {agent.name} on {len(games)} games...")
    results = []

    for i, game_id in enumerate(games, 1):
        print(f"  [{i}/{len(games)}] {game_id}...", end=" ", flush=True)
        result = run_agent_on_game(agent, game_id, args.max_steps)
        results.append(result)
        status = result.get("final_state", result.get("status", "unknown"))
        print(f"{status} ({result.get('steps', 0)} steps)")

    # Summary
    wins = sum(1 for r in results if r.get("final_state") == "win")
    errors = sum(1 for r in results if r.get("status") == "error")
    print(f"\nResults: {wins}/{len(results)} wins, {errors} errors")

    # Save
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    submission = {
        "agent": agent.name,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "total_games": len(results),
        "wins": wins,
        "errors": errors,
        "results": results,
    }
    output_path.write_text(json.dumps(submission, indent=2))
    print(f"Saved to {args.output}")


if __name__ == "__main__":
    main()
