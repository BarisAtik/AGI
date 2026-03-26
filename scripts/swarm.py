#!/usr/bin/env python3
"""Multi-game swarm runner — runs an agent across many games concurrently.

Usage:
    python scripts/swarm.py --agent=dfs --games ls20 ft09 --workers=4
    python scripts/swarm.py --agent=astar --all --output=results/swarm.json
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def run_single_game(agent_name: str, game_id: str, max_steps: int, max_depth: int) -> dict:
    """Run a single agent-game pair. Designed for process pool execution."""
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

        frames: list[FrameData] = [FrameData(frame_number=0)]
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

        elapsed = time.time() - start
        return {
            "game_id": game_id,
            "agent": agent_name,
            "status": "completed",
            "steps": step,
            "elapsed_seconds": round(elapsed, 2),
            "final_state": frames[-1].state.value,
            "levels_completed": frames[-1].levels_completed,
            "win_levels": frames[-1].win_levels,
        }

    except ImportError:
        return {
            "game_id": game_id,
            "agent": agent_name,
            "status": "no_sdk",
            "elapsed_seconds": round(time.time() - start, 2),
        }
    except Exception as e:
        return {
            "game_id": game_id,
            "agent": agent_name,
            "status": "error",
            "error": str(e),
            "elapsed_seconds": round(time.time() - start, 2),
        }


def main():
    parser = argparse.ArgumentParser(description="Multi-game swarm runner")
    parser.add_argument("--agent", default="dfs", choices=["random", "dfs", "bfs", "astar"])
    parser.add_argument("--games", nargs="*", help="Game IDs to run")
    parser.add_argument("--all", action="store_true", help="Run all available games")
    parser.add_argument("--workers", type=int, default=4, help="Parallel workers")
    parser.add_argument("--max-steps", type=int, default=1000)
    parser.add_argument("--max-depth", type=int, default=50)
    parser.add_argument("--output", default="results/swarm.json")
    args = parser.parse_args()

    games = args.games or []

    if args.all or not games:
        try:
            from arc_agi import Arcade

            arc = Arcade()
            game_list = arc.list_games() if hasattr(arc, "list_games") else []
            games = [g.id if hasattr(g, "id") else str(g) for g in game_list]
        except ImportError:
            pass

    if not games:
        print("No games specified. Use --games or --all with arc-agi SDK installed.")
        sys.exit(1)

    print(f"Swarm: {args.agent} agent x {len(games)} games ({args.workers} workers)")
    results = []
    start = time.time()

    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(run_single_game, args.agent, gid, args.max_steps, args.max_depth): gid
            for gid in games
        }
        for future in as_completed(futures):
            gid = futures[future]
            try:
                result = future.result()
                results.append(result)
                state = result.get("final_state", result.get("status"))
                steps = result.get("steps", "?")
                print(f"  {gid}: {state} ({steps} steps)")
            except Exception as e:
                print(f"  {gid}: FAILED ({e})")
                results.append({"game_id": gid, "status": "crash", "error": str(e)})

    total_time = round(time.time() - start, 2)
    wins = sum(1 for r in results if r.get("final_state") == "win")
    print(f"\nDone in {total_time}s: {wins}/{len(results)} wins")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps({
        "agent": args.agent,
        "total_games": len(results),
        "wins": wins,
        "total_seconds": total_time,
        "results": results,
    }, indent=2))
    print(f"Saved to {args.output}")


if __name__ == "__main__":
    main()
