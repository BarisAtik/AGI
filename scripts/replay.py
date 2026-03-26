#!/usr/bin/env python3
"""Replay and analyze recorded game runs.

Records agent decisions and allows replaying them for debugging and analysis.

Usage:
    # Record a run
    python scripts/replay.py record --agent=dfs --game=ls20 --output=replays/dfs_ls20.json

    # Analyze a recording
    python scripts/replay.py analyze --input=replays/dfs_ls20.json
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def record_run(agent_name: str, game_id: str, max_steps: int, max_depth: int) -> dict:
    """Record a full agent run with action-by-action detail."""
    from agents import AVAILABLE_AGENTS
    from agents.structs import FrameData, GameAction, GameState

    agent_cls = AVAILABLE_AGENTS[agent_name]
    if agent_name in ("dfs", "astar"):
        agent = agent_cls(max_depth=max_depth, max_steps=max_steps)
    elif agent_name == "bfs":
        agent = agent_cls(max_depth=max_depth, max_steps=max_steps)
    else:
        agent = agent_cls(max_steps=max_steps)

    agent.reset()
    start = time.time()
    actions_log = []

    try:
        from arc_agi import Arcade
        from arc_agi.types import GameAction as SDKGameAction

        arc = Arcade()
        env = arc.make(game_id, render_mode="terminal")

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

        frames: list[FrameData] = [FrameData(frame_number=0)]
        step = 0

        while not agent.is_done(frames, frames[-1]):
            action = agent.choose_action(frames, frames[-1])
            sdk_action = sdk_map[action.action]

            action_entry = {
                "step": step + 1,
                "action": action.action.name,
                "reasoning": action.reasoning,
                "data": action.data,
                "timestamp": round(time.time() - start, 3),
            }

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

            action_entry["result_state"] = frame.state.value
            action_entry["levels_completed"] = frame.levels_completed
            actions_log.append(action_entry)

        return {
            "agent": agent_name,
            "game": game_id,
            "total_steps": step,
            "elapsed_seconds": round(time.time() - start, 2),
            "final_state": frames[-1].state.value,
            "levels_completed": frames[-1].levels_completed,
            "actions": actions_log,
        }

    except ImportError:
        # Standalone mode — record actions without SDK
        frames: list[FrameData] = [FrameData(frame_number=0)]
        step = 0

        while not agent.is_done(frames, frames[-1]):
            action = agent.choose_action(frames, frames[-1])
            step += 1
            actions_log.append({
                "step": step,
                "action": action.action.name,
                "reasoning": action.reasoning,
                "data": action.data,
                "timestamp": round(time.time() - start, 3),
            })
            frames.append(FrameData(frame_number=step))

        return {
            "agent": agent_name,
            "game": game_id,
            "mode": "standalone",
            "total_steps": step,
            "elapsed_seconds": round(time.time() - start, 2),
            "actions": actions_log,
        }


def analyze_recording(data: dict):
    """Print analysis of a recorded run."""
    print(f"Agent: {data['agent']}")
    print(f"Game:  {data['game']}")
    print(f"Steps: {data['total_steps']}")
    print(f"Time:  {data.get('elapsed_seconds', '?')}s")
    print(f"Final: {data.get('final_state', data.get('mode', '?'))}")
    print()

    # Action distribution
    actions = data.get("actions", [])
    action_counts: dict[str, int] = {}
    for a in actions:
        name = a["action"]
        action_counts[name] = action_counts.get(name, 0) + 1

    print("Action Distribution:")
    for name, count in sorted(action_counts.items(), key=lambda x: -x[1]):
        pct = 100 * count / len(actions) if actions else 0
        bar = "#" * int(pct / 2)
        print(f"  {name:10s} {count:5d} ({pct:5.1f}%) {bar}")

    # Backtrack ratio
    undos = action_counts.get("ACTION7", 0)
    if actions:
        print(f"\nBacktrack ratio: {undos}/{len(actions)} ({100*undos/len(actions):.1f}%)")

    # Reasoning patterns
    reasoning_counts: dict[str, int] = {}
    for a in actions:
        reason = a.get("reasoning", "").split("(")[0].strip()
        if reason:
            reasoning_counts[reason] = reasoning_counts.get(reason, 0) + 1

    if reasoning_counts:
        print("\nReasoning Patterns:")
        for reason, count in sorted(reasoning_counts.items(), key=lambda x: -x[1])[:10]:
            print(f"  {reason}: {count}")


def main():
    parser = argparse.ArgumentParser(description="Replay and analyze game runs")
    sub = parser.add_subparsers(dest="command")

    rec = sub.add_parser("record", help="Record an agent run")
    rec.add_argument("--agent", default="dfs", choices=["random", "dfs", "bfs", "astar"])
    rec.add_argument("--game", required=True)
    rec.add_argument("--max-steps", type=int, default=1000)
    rec.add_argument("--max-depth", type=int, default=50)
    rec.add_argument("--output", required=True)

    ana = sub.add_parser("analyze", help="Analyze a recording")
    ana.add_argument("--input", required=True)

    args = parser.parse_args()

    if args.command == "record":
        data = record_run(args.agent, args.game, args.max_steps, args.max_depth)
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(data, indent=2))
        print(f"Recorded {data['total_steps']} steps to {args.output}")
        analyze_recording(data)

    elif args.command == "analyze":
        data = json.loads(Path(args.input).read_text())
        analyze_recording(data)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
