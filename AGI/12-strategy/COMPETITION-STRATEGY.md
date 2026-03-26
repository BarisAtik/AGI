# ARC-AGI Competition Strategy: The Winning Playbook
## Synthesized from 360+ Sources Across Papers, Winners, and Community Research

**Compiled**: March 26, 2026
**Purpose**: Definitive strategy guide for competing in ARC Prize 2026
**Tracks**: ARC-AGI-3 (interactive agents) + ARC-AGI-2 (static reasoning)

---

## THE LANDSCAPE AT A GLANCE

### What We're Up Against

| Benchmark | Human Baseline | Best AI | Frontier LLMs | Gap |
|-----------|---------------|---------|----------------|-----|
| ARC-AGI-1 | 85% | 55.5% (MindsAI) | 5% (GPT-4o raw) | Narrowing |
| ARC-AGI-2 | 60% | 24% (NVARC) | 0% (raw LLMs) | Massive |
| ARC-AGI-3 | 100% | 12.58% (StochasticGoose) | <1% | Enormous |

**Source**: ARC Prize 2025 Technical Report (arXiv:2601.10904), ARC-AGI-3 Preview Results (arcprize.org/blog/arc-agi-3-preview-30-day-learnings)

### The Competition Structure (ARC Prize 2026)

- **Total Prize Pool**: $2,000,000 across 3 tracks
- **Deadline**: November 2, 2026 (milestones June 30 & Sept 30)
- **Constraints**: Offline execution only (no API calls), open-source mandatory, 12-hour Kaggle runtime, reproducible
- **Scoring (AGI-3)**: Quadratic efficiency metric — (human_actions / ai_actions)². Every wasted action costs quadratically.

**Source**: ARC Prize 2026 Kaggle page (kaggle.com/competitions/arc-prize-2026-arc-agi-3), ARC Prize Policy (arcprize.org/policy)

---

## PART 1: ARC-AGI-2 TRACK STRATEGY (Static Reasoning)

### The Proven Formula: What Winners Actually Do

Every top solution since 2024 follows the same meta-pattern, confirmed across all winning writeups:

```
Synthetic Data Generation → Pre-training → Test-Time Training → Ensemble Voting
```

No static inference solution has ever scored above 11%. TTT is not optional — it is the minimum viable technique.

**Source**: ARC Prize 2024 Winners Technical Report (arcprize.org/blog/arc-prize-2024-winners-technical-report), Living Survey of 82 approaches (arXiv:2603.13372)

### Technique Stack Ranked by Impact

| Technique | Impact (pp gain) | Difficulty | Used By |
|-----------|-----------------|------------|---------|
| Test-Time Training (TTT) | +30-40pp | High | All winners |
| Data Augmentation (1000×) | +11-20pp | Medium | All winners |
| 2D Position Encodings | +5-10pp | Medium | ARChitects, NVARC |
| Ensemble (TTT + TRM) | +5pp | Medium | NVARC (1st 2025) |
| Synthetic Pre-training (100K tasks) | +10-15pp | High | NVARC (1st 2025) |
| Recursive Refinement + Deep Supervision | +10pp (2× accuracy) | Medium | TRM (Best Paper 2025) |
| Program Synthesis (LLM-guided) | Complementary coverage | High | Greenblatt (42%) |

**Source**: Compiled from TTT paper (arXiv:2411.07279), TRM paper (arXiv:2510.04871), NVARC GitHub (github.com/1ytic/NVARC)

### Architecture Blueprint

**Recommended: Three-Module Ensemble**

#### Module 1: TTT Transduction Engine
- Base: 4B parameter model (Qwen-family, following NVARC pattern)
- LoRA adapters (rank 16) on K, Q, V, O matrices — task-specific
- Pre-trained on 100K+ synthetic ARC-like puzzles
- At test time: 2 epochs fine-tuning per task on augmented demonstrations
- Augmentation: Dihedral symmetries, color permutations, translations (1000× per example)

**Why 4B not 8B?** NVARC won at $0.20/task with 4B, beating 8B solutions. Efficiency wins.

**Source**: NVARC solution (github.com/1ytic/NVARC), TTT paper (arXiv:2411.07279)

#### Module 2: Tiny Recursive Model (TRM)
- 7M parameters, 2 layers
- Recursive refinement loop (≤16 steps): z' = f_think(x, y, z), y' = f_act(y, z')
- Deep supervision at EVERY step (this doubled accuracy vs. single-step)
- Learned halting mechanism
- Solves different task distribution than TTT — orthogonal coverage

**Key insight**: This 7M model outperforms DeepSeek-R1 (671B), Gemini 2.5 Pro, and o3-mini on ARC.

**Source**: TRM paper "Less is More" (arXiv:2510.04871), Samsung SAIL Montreal

#### Module 3: LLM-Guided Program Synthesis
- Local LLM generates Python programs that transform input → output
- Generate k=2048 candidate programs per task
- Validate against provided examples
- Iterative debugging of most promising candidates
- Log-linear scaling: more samples → logarithmic accuracy gain

**Why include this?** Solves fundamentally different tasks than transduction. TTT excels at visual/spatial; synthesis excels at symbolic/logical.

**Source**: Ryan Greenblatt's approach (blog.redwoodresearch.org), SOAR paper (arXiv:2507.14172)

#### Ensemble Strategy
- Weighted voting across all three modules
- Confidence-based weighting (higher-confidence predictions get more weight)
- Perspective transforms: run each module on rotated/reflected versions of input
- Final selection: majority vote or highest-confidence prediction

**Source**: NVARC ensemble design, ARChitects 2025 perspective-based scoring

### Synthetic Data: The Hidden Weapon

NVARC's key insight: move reasoning offline into data generation.

- **RE-ARC** (github.com/michaelhodel/re-arc): Procedural generators for 400,000 verified synthetic tasks
- **ARC-GEN** (github.com/google/ARC-GEN): Google's 100K+ pre-generated examples
- **ARC-TGI** (arXiv:2603.05099): 461 human-validated task generators with reasoning chain templates
- **Concept decomposition**: Break ARC into fundamental mechanics, recombine for diversity

**Source**: RE-ARC repo, ARC-GEN repo, ARC-TGI paper

### What Will NOT Work (Avoid These)

1. **Pure LLM prompting**: 0% on ARC-AGI-2 without TTT (Source: Living Survey, arXiv:2603.13372)
2. **Brute-force program search**: Combinatorial explosion, tasks designed to resist this (Source: ARC-AGI-2 paper, arXiv:2505.11831)
3. **Single-model solutions**: No single technique exceeds ~40% alone (Source: competition results analysis)
4. **Scaling without adaptation**: 20% ceiling for pure neural, regardless of size (Source: Living Survey)
5. **o3-style compute burn**: $3,460/task is not competitive when budget is $0.20/task (Source: o3 analysis, arXiv:2501.07458)

---

## PART 2: ARC-AGI-3 TRACK STRATEGY (Interactive Agents)

### The Paradigm Shift

ARC-AGI-3 is fundamentally different. No input/output pairs. No instructions. No stated goals. Agents must:
1. **Perceive** 64×64 RGB frames (16-color palette)
2. **Explore** by taking actions (arrows or clicks)
3. **Discover** game rules through experimentation
4. **Execute** solutions efficiently

Scoring: (human_actions / ai_actions)² — quadratic penalty for wasted exploration.

**Source**: ARC-AGI-3 Technical Docs (docs.arcprize.org), Preview competition results

### What Won the Preview Competition

**1st Place: StochasticGoose (12.58%)** — CNN with action-learning
- NOT an LLM approach. CNN-based structured exploration beat GPT-5.x by 12+ points
- Learned which actions impact state through visual change detection
- Explicit state tracking

**3rd Place: Graph-Based Exploration (57.7% success rate on solved levels)**
- Explicit state graph construction
- Visual change detection between frames
- Systematic exploration of action effects

**Source**: Dries Smit's 1st place writeup (medium.com/@dries.epos), Graph-Based Exploration paper (arXiv:2512.24156)

### Agent Architecture Blueprint

```
                    ┌─────────────────────┐
                    │   Vision Module     │
                    │  (CNN/ViT on 64×64) │
                    └──────┬──────────────┘
                           │
                    ┌──────▼──────────────┐
                    │   State Tracker     │
                    │  (State Graph +     │
                    │   Change Detection) │
                    └──────┬──────────────┘
                           │
              ┌────────────▼────────────────┐
              │    World Model Builder      │
              │  (Hypothesis about rules,   │
              │   goals, mechanics)         │
              └────────────┬────────────────┘
                           │
              ┌────────────▼────────────────┐
              │    Action Planner           │
              │  (Minimize exploration,     │
              │   maximize information)     │
              └────────────┬────────────────┘
                           │
              ┌────────────▼────────────────┐
              │    Execution Engine         │
              │  (Apply learned strategy    │
              │   efficiently)              │
              └─────────────────────────────┘
```

### Key Design Principles for AGI-3

1. **Vision-First**: Strong CNN perception is essential. 16-color discrete palette simplifies processing. All frontier LLMs failed (<1%) — visual reasoning is the bottleneck.

2. **Structured Exploration**: Random exploration is quadratically penalized. Use information-theoretic action selection: choose actions that maximize expected information gain about game mechanics.

3. **State Tracking**: Build an explicit state graph. Detect what changed between frames. Track which actions have which effects. The 3rd-place graph approach had 57.7% level success rate.

4. **Progressive Complexity**: Games have 8-10 levels with new mechanics per level. Agent must detect when new rules appear and adapt without forgetting old ones.

5. **Efficiency Over Completeness**: Better to solve fewer levels perfectly (high efficiency score) than many levels poorly. The quadratic metric means 50% efficiency on 6 levels beats 25% efficiency on 12 levels.

**Source**: H-ARC human performance study (arXiv:2409.01374), ARC-AGI-3 preview learnings, StochasticGoose solution

### Action Spaces

| Game Type | Action Space | Strategy |
|-----------|-------------|----------|
| Arrow-based (ls20) | 4 actions | Systematic grid traversal, state mapping |
| Click-based (ft09, vc33, lp85) | 4,096 actions (64×64) | Attention-guided clicking, region-based exploration |

**Source**: ARC-AGI-3 Technical Documentation (docs.arcprize.org)

---

## PART 3: CROSS-CUTTING INSIGHTS

### Why LLMs Fail on ARC (and What This Means for Us)

**o3's paradox**: 87.5% on AGI-1, but 2.9% on AGI-2 and <1% on AGI-3.

The failure pattern reveals exactly what's hard:
- **Symbol semantics**: Assigning meaning beyond visual patterns (30-40% of AGI-2 tasks)
- **Multi-rule composition**: Applying multiple interacting rules simultaneously
- **Context-dependent rules**: Same symbol, different rule depending on context
- **Autonomous learning**: Discovering rules without instructions (AGI-3)

**Strategic implication**: Don't build an LLM-only solution. Use LLMs for what they're good at (program generation, hypothesis formation) but combine with specialized perception and reasoning.

**Source**: o3 analysis (arXiv:2501.07458), LLM reasoning analysis (arXiv:2403.11793), Mikel Bober-Irizar unsolved tasks analysis

### Core Knowledge Priors (The Rulebook)

Chollet's four priors define the scope of ARC tasks. Any solver MUST handle all four:

1. **Objectness & Physics**: Objects cohere, persist, interact via contact, can't pass through each other
2. **Agentness & Goals**: Intentional agents, goal-directed behavior, action understanding
3. **Numbers & Arithmetic**: Counting, cardinality, basic operations, conservation
4. **Geometry & Topology**: Spatial relationships, shapes, connectivity, symmetry, transformations

**Source**: "On the Measure of Intelligence" (arXiv:1911.01547)

### The Efficiency Imperative

Both tracks reward efficiency over raw accuracy:
- AGI-2: $0.20/task budget wins over $5/task
- AGI-3: Quadratic penalty for exploration waste
- NVARC's 4B model beat 8B models at 1/5th the cost
- TRM's 7M model beat 671B models on reasoning

**Lesson**: Algorithm > Scale. Every architectural decision should ask "does this make us more efficient?"

**Source**: NVARC cost analysis, TRM paper, ARC Prize 2025 results

---

## PART 4: IMPLEMENTATION ROADMAP

### Phase 1: Foundation (Weeks 1-3)
- [ ] Set up Kaggle notebook environment, test offline execution
- [ ] Download and explore ARC-AGI-2 dataset (github.com/arcprize/ARC-AGI-2)
- [ ] Install ARC-AGI-3 toolkit (github.com/arcprize/ARC-AGI-3-Agents)
- [ ] Implement baseline TTT with LoRA on small model
- [ ] Build basic data augmentation pipeline (geometric transforms)

### Phase 2: Core Development (Weeks 4-8)
- [ ] Train/fine-tune 4B model on synthetic ARC data (RE-ARC + ARC-GEN)
- [ ] Implement TRM module (7M params, recursive refinement, deep supervision)
- [ ] Build program synthesis pipeline with local LLM
- [ ] For AGI-3: Build CNN vision module + state tracker + change detection
- [ ] Implement ensemble voting across modules

### Phase 3: Optimization (Weeks 9-12)
- [ ] Generate 100K+ synthetic puzzles via concept decomposition
- [ ] Tune augmentation strategies per task type
- [ ] For AGI-3: Implement information-theoretic exploration strategy
- [ ] Optimize compute budget (target $0.20/task for AGI-2)
- [ ] Run on private evaluation, iterate on failure modes

### Phase 4: Competition (Weeks 13-16)
- [ ] Full evaluation on Kaggle (12-hour limit test)
- [ ] Ablation studies: which components contribute most
- [ ] Final ensemble weight tuning
- [ ] Documentation for open-source release
- [ ] Submit for June 30 milestone

---

## PART 5: KEY REPOSITORIES TO USE

| Repository | Purpose | URL |
|-----------|---------|-----|
| ARC-AGI-3-Agents | Official agent template | github.com/arcprize/ARC-AGI-3-Agents |
| ARC-AGI-2 Dataset | Training + eval tasks | github.com/arcprize/ARC-AGI-2 |
| NVARC | 1st place 2025 solution | github.com/1ytic/NVARC |
| StochasticGoose | 1st place AGI-3 preview | github.com/DriesSmit/ARC3-solution |
| ARC-DSL | Domain-specific language | github.com/michaelhodel/arc-dsl |
| RE-ARC | 400K synthetic tasks | github.com/michaelhodel/re-arc |
| ARC-GEN | Google's 100K+ examples | github.com/google/ARC-GEN |
| ARCKit | Dataset tools | github.com/mxbi/arckit |
| SakanaAI AB-MCTS | Multi-LLM MCTS | github.com/SakanaAI/ab-mcts-arc2 |
| epang080516 arc_agi | 77.1% program synthesis | github.com/epang080516/arc_agi |

---

## PART 6: THE WINNING EDGE — WHAT MOST TEAMS MISS

Based on analyzing all 82 approaches in the living survey and all winning solutions:

### 1. Deep Supervision is Underrated
TRM doubled its accuracy just by adding loss at every recursive step. Most teams skip this. It's low-effort, high-impact.

### 2. Synthetic Data Quality > Quantity
NVARC's 103K carefully composed puzzles beat teams with millions of random augmentations. Concept decomposition and recombination is the key.

### 3. The Transduction-Induction Split
TTT and program synthesis solve fundamentally different task types. Teams that use only one approach leave ~40% of tasks unsolvable. Ensemble both.

### 4. 2D is Not a Gimmick
Replacing 1D positional encodings with 2D variants consistently adds 5-10 percentage points. ARC is a spatial problem — treat it spatially.

### 5. For AGI-3: Don't Use LLMs as Agents
Every LLM-based agent scored <1% in the preview. CNN-based perception + structured exploration is the proven path. LLMs can help with strategy formulation offline, but the runtime agent should be neural/algorithmic.

### 6. Efficiency is a Feature, Not a Constraint
The cheapest solution (NVARC, $0.20/task) also won. Efficiency forces you to build smarter architectures instead of throwing compute at the problem.

---

## SOURCES INDEX

All research notes with full source citations are organized in the project directory:

| Folder | Contents |
|--------|----------|
| `01-competition-overview/` | Competition rules, format, scoring, timeline |
| `02-foundational-papers/` | Chollet's intelligence paper, AGI-2 paper, living survey |
| `03-winning-solutions/` | Detailed winner analysis + quick reference |
| `04-test-time-training/` | TTT approaches, TRM, augmentation strategies |
| `05-program-synthesis/` | ILP, SOAR, ConceptSearch, DreamCoder |
| `06-llm-approaches/` | LLM reasoning analysis, Product of Experts, neuro-symbolic |
| `07-neural-approaches/` | ViT, NCA, GPAR, Vector Symbolic Algebras |
| `08-neuro-symbolic/` | Human cognition, agent design patterns, H-ARC |
| `09-o3-analysis/` | o3 breakthrough, failure on AGI-2/3, compute costs |
| `10-community-insights/` | Blog posts, strategic analyses, community wisdom |
| `11-tools-and-repos/` | GitHub inventory, datasets, frameworks |
| `12-strategy/` | This document |

---

*Built from 360+ sources. Every claim is backed by citations in the individual research files. Let's win this.*
