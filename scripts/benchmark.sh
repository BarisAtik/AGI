#!/usr/bin/env bash
# Benchmark agents across multiple games
# Usage: ./scripts/benchmark.sh [agent] [game1 game2 ...]

set -euo pipefail

AGENT="${1:-dfs}"
shift || true
GAMES="${@:-ls20}"

echo "=== ARC-AGI-3 Benchmark ==="
echo "Agent: $AGENT"
echo "Games: $GAMES"
echo ""

mkdir -p results

for game in $GAMES; do
    echo "--- Running $AGENT on $game ---"
    uv run main.py --agent="$AGENT" --game="$game" \
        --output="results/${AGENT}_${game}.json" \
        2>&1 | tail -8
    echo ""
done

echo "Results saved to results/"
