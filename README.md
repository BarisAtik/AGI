# ARC-AGI-3 Solver

Systematic solver for the [ARC Prize 2026](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3/overview) competition (ARC-AGI-3), with [nightshift](https://github.com/marcus/nightshift)-powered continuous improvement.

## What is ARC-AGI-3?

ARC-AGI-3 is the first **interactive** reasoning benchmark — agents explore novel game environments, acquire goals on the fly, and learn continuously. Unlike static puzzles, agents must perceive, act, and adapt through experience with 7 action types (directional, interact, coordinate-based, undo).

Key properties:
- 100% human-solvable environments
- Scoring based on skill-acquisition efficiency over time
- Weighted game averages with squared individual level scores

## Project Structure

```
├── agents/
│   ├── agent.py          # Base agent class
│   ├── structs.py        # FrameData, GameAction, GameState
│   ├── random_agent.py   # Random baseline
│   └── dfs_agent.py      # Depth-first search solver
├── kaggle/
│   └── submit.py         # Kaggle submission pipeline
├── tests/                # Test suite
├── scripts/              # Utility scripts
├── .nightshift/          # Nightshift config for automated improvement
├── .claude/skills/       # Claude Code skills for the project
├── main.py               # CLI entry point
└── pyproject.toml        # Python project config
```

## Quick Start

```bash
# Install dependencies
uv sync

# Set up API key
cp .env.example .env
# Edit .env with your key from https://three.arcprize.org/

# Run DFS agent on a game
uv run main.py --agent=dfs --game=ls20 --render

# Run random baseline
uv run main.py --agent=random --game=ft09

# Run tests
uv run pytest
```

## Agents

| Agent | Strategy | Use Case |
|-------|----------|----------|
| `random` | Random action selection | Baseline / sanity check |
| `dfs` | Depth-first search with backtracking | Systematic exploration |

### DFS Agent

The DFS agent treats each game as a search problem:
1. Explores actions depth-first using a configurable priority order
2. Tracks visited states via grid hashing to avoid cycles
3. Backtracks via ACTION7 (undo) when hitting depth limits or revisited states
4. Configurable max depth and step budget

```bash
uv run main.py --agent=dfs --game=ls20 --max-depth=30 --max-steps=500
```

## Kaggle Submission

```bash
# Run against specific games
python kaggle/submit.py --agent=dfs --games ls20 ft09

# Output saved to kaggle/submission/results.json
```

## Nightshift (Automated Improvement)

[Nightshift](https://github.com/marcus/nightshift) runs overnight to find bugs, test gaps, dead code, and other issues — all delivered as PRs for review.

```bash
# Install
brew install marcus/tap/nightshift

# Setup
nightshift setup

# Preview what it will do
nightshift preview

# Run immediately
nightshift run
```

Config lives in `.nightshift/config.yaml`.

## Roadmap

- [x] Project scaffolding and agent framework
- [x] DFS baseline agent
- [x] Kaggle submission pipeline
- [x] Nightshift integration
- [ ] State evaluation heuristics for smarter pruning
- [ ] BFS and A* search variants
- [ ] LLM-guided action selection
- [ ] Pattern recognition from frame history
- [ ] Multi-game performance benchmarking
- [ ] Kaggle leaderboard push
