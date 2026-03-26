# ARC-AGI-3 Solver Project

## Overview
This project solves ARC-AGI-3 interactive reasoning benchmark games using
search-based agents. The competition runs on Kaggle (ARC Prize 2026).

## Architecture
- `agents/` — Agent implementations (base class, DFS, random)
- `agents/structs.py` — Core data structures (FrameData, GameAction, GameState)
- `main.py` — CLI entry point
- `kaggle/` — Kaggle submission pipeline
- `tests/` — Test suite

## Key Concepts
- ARC-AGI-3 is an **interactive** benchmark (not static puzzles)
- Agents interact with game environments via step-based actions
- 7 action types: directional (1-4), interact (5), coordinate (6), undo (7)
- Games have levels; scoring uses weighted averages with squared level scores
- SDK: `arc-agi` Python package, main class is `Arcade()`

## Running
```bash
uv run main.py --agent=dfs --game=ls20
uv run main.py --agent=random --game=ft09 --render
```

## Improvement Areas
- Better state heuristics for DFS pruning
- BFS/A* search variants
- LLM-guided action selection
- Pattern recognition from frame history
- Multi-game performance optimization
