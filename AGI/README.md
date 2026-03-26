# ARC-AGI Competition Research Hub
## Complete Research for ARC Prize 2026

**Compiled**: March 26, 2026
**Sources**: 360+ links from the ARC-AGI Complete Resource Guide
**Goal**: Competition-winning strategy for ARC Prize 2026 ($2M prize pool)

---

## Quick Start

**Read first**: `12-strategy/COMPETITION-STRATEGY.md` — the synthesized playbook

Then dive into specific topics as needed:

## Directory Structure

```
AGI/
├── README.md                          ← You are here
├── 01-competition-overview/           ← Rules, format, scoring, timeline
│   └── competition-rules-and-format.md
├── 02-foundational-papers/            ← Chollet, AGI-2, living survey (82 approaches)
│   └── foundational-research-notes.md
├── 03-winning-solutions/              ← Detailed winner blueprints
│   ├── winning-solutions-analysis.md  ← Main technical analysis
│   ├── QUICK_REFERENCE.md             ← Fast lookup
│   └── README.md
├── 04-test-time-training/             ← TTT, TRM, augmentation
│   └── ttt-approaches-notes.md
├── 05-program-synthesis/              ← ILP, SOAR, ConceptSearch, DreamCoder
│   └── program-synthesis-notes.md
├── 06-llm-approaches/                 ← LLM analysis, Product of Experts, neuro-symbolic
│   ├── llm-and-neurosymbolic-notes.md
│   └── README.md
├── 07-neural-approaches/              ← ViT, NCA, GPAR, Vector Symbolic Algebras
│   └── neural-approaches-notes.md
├── 08-neuro-symbolic/                 ← Human cognition, agent design, H-ARC
│   └── human-cognition-and-agent-design.md
├── 09-o3-analysis/                    ← o3 breakthrough and failure analysis
│   └── o3-breakthrough-analysis.md
├── 10-community-insights/             ← Blog posts, strategic analyses
│   └── blog-posts-and-analyses.md
├── 11-tools-and-repos/                ← GitHub repos, datasets, frameworks
│   └── github-repos-inventory.md
└── 12-strategy/                       ← THE PLAYBOOK
    └── COMPETITION-STRATEGY.md
```

## Key Numbers

- **ARC-AGI-2 SOTA**: 24% (NVARC, $0.20/task)
- **ARC-AGI-3 SOTA**: 12.58% (StochasticGoose, CNN agent)
- **Human baselines**: 60% (AGI-2), 100% (AGI-3)
- **Prize pool**: $2,000,000
- **Deadline**: November 2, 2026

## The One-Line Strategy

**AGI-2**: Synthetic data → TTT (4B model + LoRA) + TRM (7M recursive) + Program Synthesis → Ensemble

**AGI-3**: CNN perception → State graph → Structured exploration → Efficient execution
