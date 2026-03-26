#!/usr/bin/env python3
"""ARC-AGI-3 Solver — main entry point.

Usage:
    uv run main.py --agent=dfs --game=ls20
    uv run main.py --agent=random --game=ft09 --render
    uv run main.py --agent=dfs --game=ls20 --max-depth=30 --max-steps=500
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="ARC-AGI-3 Solver")
    parser.add_argument(
        "--agent",
        type=str,
        default="dfs",
        choices=["random", "dfs"],
        help="Agent to use (default: dfs)",
    )
    parser.add_argument(
        "--game",
        type=str,
        required=True,
        help="Game ID to play (e.g., ls20, ft09)",
    )
    parser.add_argument(
        "--render",
        action="store_true",
        help="Enable terminal rendering",
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=50,
        help="DFS max search depth (default: 50)",
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=1000,
        help="Max steps per episode (default: 1000)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Path to save results JSON",
    )
    return parser.parse_args()


def create_agent(args: argparse.Namespace):
    from agents import AVAILABLE_AGENTS

    agent_cls = AVAILABLE_AGENTS[args.agent]
    if args.agent == "dfs":
        return agent_cls(max_depth=args.max_depth, max_steps=args.max_steps)
    elif args.agent == "random":
        return agent_cls(max_steps=args.max_steps)
    return agent_cls()


def run_with_sdk(args: argparse.Namespace) -> dict:
    """Run an agent against a game using the arc-agi SDK."""
    from arc_agi import Arcade
    from arc_agi.types import GameAction as SDKGameAction

    from agents.structs import FrameData, GameAction, GameState

    agent = create_agent(args)
    agent.reset()

    render_mode = "terminal" if args.render else None
    arc = Arcade()
    env = arc.make(args.game, render_mode=render_mode)

    # Map our GameAction to SDK GameAction
    sdk_action_map = {
        GameAction.RESET: SDKGameAction.RESET,
        GameAction.ACTION1: SDKGameAction.ACTION1,
        GameAction.ACTION2: SDKGameAction.ACTION2,
        GameAction.ACTION3: SDKGameAction.ACTION3,
        GameAction.ACTION4: SDKGameAction.ACTION4,
        GameAction.ACTION5: SDKGameAction.ACTION5,
        GameAction.ACTION6: SDKGameAction.ACTION6,
        GameAction.ACTION7: SDKGameAction.ACTION7,
    }

    frames: list[FrameData] = []
    start_time = time.time()

    # Initial observation
    initial_frame = FrameData(frame_number=0)
    frames.append(initial_frame)

    step = 0
    while True:
        latest = frames[-1]
        if agent.is_done(frames, latest):
            break

        action_with_data = agent.choose_action(frames, latest)
        sdk_action = sdk_action_map[action_with_data.action]

        if action_with_data.data:
            obs = env.step(sdk_action, data=action_with_data.data)
        else:
            obs = env.step(sdk_action)

        step += 1
        frame = FrameData(
            frame_number=step,
            state=GameState(obs.state.value) if hasattr(obs, "state") else GameState.RUNNING,
            levels_completed=getattr(obs, "levels_completed", 0),
            win_levels=getattr(obs, "win_levels", 1),
            available_actions=[],
            grid=getattr(obs, "grid", None),
            render=getattr(obs, "render", ""),
        )
        frames.append(frame)

        if args.render and frame.render:
            print(frame.render)

    elapsed = time.time() - start_time
    scorecard = arc.get_scorecard()

    result = {
        "agent": agent.name,
        "game": args.game,
        "steps": len(frames) - 1,
        "elapsed_seconds": round(elapsed, 2),
        "final_state": frames[-1].state.value,
        "levels_completed": frames[-1].levels_completed,
        "scorecard": scorecard if isinstance(scorecard, dict) else str(scorecard),
    }

    print(f"\n{'='*50}")
    print(f"Agent: {result['agent']}")
    print(f"Game:  {result['game']}")
    print(f"Steps: {result['steps']}")
    print(f"Time:  {result['elapsed_seconds']}s")
    print(f"State: {result['final_state']}")
    print(f"Levels: {result['levels_completed']}")
    print(f"{'='*50}")

    return result


def run_standalone(args: argparse.Namespace) -> dict:
    """Run agent in standalone mode without the SDK (for testing/development)."""
    from agents.structs import FrameData, GameState

    agent = create_agent(args)
    agent.reset()

    print(f"[standalone] Running {agent.name} on game '{args.game}' (no SDK)")
    print(f"[standalone] max_steps={args.max_steps}, max_depth={getattr(agent, 'max_depth', 'N/A')}")

    frames: list[FrameData] = []
    frame = FrameData(frame_number=0, available_actions=[])
    frames.append(frame)

    step = 0
    while not agent.is_done(frames, frames[-1]):
        action = agent.choose_action(frames, frames[-1])
        step += 1
        # In standalone mode we just simulate — state doesn't change
        frame = FrameData(frame_number=step, available_actions=[])
        frames.append(frame)

        if step % 100 == 0:
            print(f"  step {step}: action={action.action.name}, reason={action.reasoning}")

    result = {
        "agent": agent.name,
        "game": args.game,
        "steps": step,
        "mode": "standalone",
        "final_state": frames[-1].state.value,
    }
    print(f"[standalone] Completed: {step} steps")
    return result


def cli():
    args = parse_args()

    try:
        result = run_with_sdk(args)
    except ImportError:
        print("[warn] arc-agi SDK not installed. Running in standalone mode.")
        print("[warn] Install with: uv add arc-agi")
        result = run_standalone(args)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(result, indent=2))
        print(f"Results saved to {args.output}")

    return result


if __name__ == "__main__":
    cli()
