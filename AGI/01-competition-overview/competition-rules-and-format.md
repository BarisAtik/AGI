# ARC Prize 2026: Comprehensive Competition Research Notes

## Executive Summary

The ARC Prize 2026 offers **$2,000,000 in prizes** across 3 tracks to advance open-source AGI research. The competition features ARC-AGI-3, a revolutionary interactive reasoning benchmark that tests whether AI agents can learn to solve novel environments without instructions, instructions, or stated goals.

---

## 1. What is ARC-AGI?

### Overview
ARC (Abstraction and Reasoning Corpus) is a benchmark designed to measure artificial general intelligence by testing the ability of AI systems to deal with reasoning problems they have not been explicitly prepared for. It tests fluid intelligence and abstraction capabilities.

**Source:** [ARC Prize - What is ARC-AGI?](https://arcprize.org/arc-agi)

### Historical Context
- ARC-AGI was first introduced in 2019 by François Chollet, a Google AI researcher and creator of Keras deep learning library
- The original benchmark was published in the paper "On the Measure Of Intelligence"
- The benchmark evolves over time to remain challenging as AI systems improve

**Source:** [ARC Prize - Leaderboard](https://arcprize.org/leaderboard)

---

## 2. ARC-AGI-3 Specifically

### What Makes ARC-AGI-3 Different

**Interactive Learning Paradigm**
- ARC-AGI-1 and 2 presented closed-grid static tasks with fixed input/output pairs
- ARC-AGI-3 introduces interactive reasoning environments requiring agents to act, probe, and discover in real time
- No instructions, no descriptions, no stated win conditions
- Agents must learn from experience inside each environment

**Key Capability Requirements**
- Perceiving what matters in a visual environment
- Selecting actions to explore and understand the environment
- Adapting strategy without relying on natural-language instructions
- Building adaptable world models from visual observations

**Source:** [ARC-AGI-3 Launches - AI Agents Must Learn, Not Memorize](https://awesomeagents.ai/news/arc-agi-3-interactive-benchmark/)

### Core Philosophy
A 100% score means AI agents can beat every game as efficiently as humans. The benchmark measures not just whether agents can solve problems, but how elegantly they solve them.

**Source:** [ARC Prize 2026](https://arcprize.org/competitions/2026/arc-agi-3)

---

## 3. ARC Prize 2026 Competition Overview

### Prize Structure
- **Total Prize Pool:** $2,000,000
- **Number of Tracks:** 3 parallel tracks
- **Philosophy:** Advancing open-source AGI research

**Track Breakdown:**
1. **ARC-AGI-2 Track:** Prizes for top scores on static reasoning benchmark (~$1M implied)
2. **ARC-AGI-3 Track:** Interactive agent reasoning benchmark (~$1M implied)
3. **Paper Track:** Awards for papers advancing understanding of ARC-AGI performance

**Source:** [ARC Prize 2026](https://arcprize.org/competitions/2026)

### Key Rules

**Open Source Requirement**
- All prize-eligible solutions MUST be open sourced before receiving official private evaluation scores
- All code authored by submitter must use permissive public domain licenses (CC0 or MIT-0)
- All third-party code must be available under open-source licenses allowing public sharing

**Source:** [ARC Prize Verified Testing Policy](https://arcprize.org/policy)

**Offline Execution**
- Kaggle evaluation environment has NO internet access
- No API-based systems allowed (e.g., GPT, Claude, or other external inference endpoints)
- If an agent requires frontier model API calls to function, it will NOT qualify
- Solutions must be fully self-contained for offline execution

**Source:** [ARC Prize 2026 - Kaggle](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3)

**Submission Method**
- All submissions must be made through designated Kaggle competitions as Kaggle notebooks
- One-click runnable via Kaggle notebook to minimize debugging cycles
- Must complete execution in under 12 hours

**Source:** [ARC Prize - 2025 Competition Details](https://arcprize.org/competitions/2025/)

**Reproducibility & Verification**
- Solutions must be reproducible and fully documented
- Code will be reviewed for compliance: no sensitive logging, no unknown APIs
- Prize awards are at sole discretion of ARC Prize Inc. technical team
- Awards may be issued in fewer or greater quantities based on submission quality and spirit of the prize

**Source:** [ARC Prize - Guide](https://arcprize.org/guide)

### Timeline
- **Milestone 1:** June 30, 2026
- **Milestone 2:** September 30, 2026
- **Submission Deadline:** November 2, 2026
- **Results Announced:** December 4, 2026

**Source:** [ARC Prize 2026](https://arcprize.org/competitions/2026)

---

## 4. ARC-AGI-3 Technical Details

### Game Environment Structure

**Benchmark Composition**
- **Total Games:** 6 novel game environments
- **Public Games:** 3 games released for development (ft09, ls20, vc33)
- **Private Games:** 3 games for leaderboard rankings (sp80, lp85, as66)
- **Total Levels:** Thousands across all environments
- **Per-Game Structure:** Each game contains 8-10 levels, with successive levels introducing new mechanics

**Level Progression Example (ls20)**
- Level 1: Basic movement + transformer object to activate exit door by key shape
- Level 2: Adds energy palettes to refill step count
- Level 3: Introduces color dimension to the key
- Level 8: Partial observations only

**Source:** [ARC-AGI-3 Quickstart - ARC-AGI-3 Docs](https://docs.arcprize.org/)

### Visual Observations

**Frame Format**
- **Resolution:** 64×64 pixel RGB frames
- **Color Palette:** Discrete palette of 16 colors
- **Information:** Both game environment and status bar (steps remaining before automatic level restart)

**Source:** [ARC-AGI-3 technical research](https://arcprize.org/arc-agi/3)

### Action Spaces

**Arrow-Based Control (ls20)**
- Directional keyboard inputs: up, down, left, right
- Action space size: |A| = 4
- Used for grid-based navigation games

**Click-Based Control (ft09, vc33, lp85)**
- Agent can click any pixel location in 64×64 frame
- Action space size: |A| = 64 × 64 = 4,096
- Enables fine-grained spatial interaction

**Source:** [ARC-AGI-3 technical research](https://arcprize.org/arc-agi/3)

### Agent API

**Python Toolkit Overview**
The ARC-AGI-3 toolkit provides a Python API for interacting with environments.

**Basic Structure**
```python
import arc_agi
from arcengine import GameAction

# Create arcade instance
arc = arc_agi.Arcade()

# Make environment
env = arc.make("ls20", render_mode="terminal")

# Take actions
for _ in range(10):
    env.step(GameAction.ACTION1)

# Get performance tracking
print(arc.get_scorecard())
```

**Key API Features**
- Arcade class: Main entry point for environment interaction
- `make()`: Create specific game environments
- `step()`: Perform actions with optional data (x, y coordinates) and reasoning logs
- Optional reasoning dictionary to include in recordings

**API Key System**
- Optional ARC_API_KEY environment variable for registered access
- Anonymous key available if no API key provided
- API key registration gives access to more games at full release

**Documentation:** [ARC-AGI-3 Quickstart - ARC-AGI-3 Docs](https://docs.arcprize.org/)
**GitHub Reference:** [GitHub - arcprize/ARC-AGI](https://github.com/arcprize/ARC-AGI)

---

## 5. ARC-AGI-3 Scoring Methodology

### Efficiency Metric

**Core Concept**
The benchmark uses a quadratic efficiency metric inspired by the SPL (Success weighted by Path Length) metric from robotics navigation research. This measures how efficiently agents convert environmental information into strategies.

**Human Baseline Definition**
- Baseline = **second-best first-run human solution by action count**
- Deliberately NOT the optimal human solution
- Represents strong (but not perfect) human performance
- Based on testing ~500 humans across 90-minute sessions in San Francisco
- Diverse population recruited including unemployed and underemployed individuals

**Scoring Formula**
```
Efficiency Score per Level = (human_actions / ai_actions)²
```

**Example:**
- Human takes 10 actions, AI takes 20 actions
- AI score = (10/20)² = 0.5² = 0.25 = 25%

**Why Quadratic?**
- Rewards efficient problem-solving, not just success
- Prevents saturation—remains challenging as AI improves
- Penalizes brute-force strategies
- AI cannot score 10% by taking 10x human actions—they only get 1%

**Source:** [ARC-AGI-3: Understanding the New Benchmark](https://techplanet.today/post/arc-agi-3-understanding-the-new-benchmark-for-measuring-artificial-general-intelligence)

### Action Efficiency Framework

**Two Ways Agents Spend Actions**
1. **Exploration:** Actions spent probing the environment to understand rules and mechanics
2. **Execution:** Actions spent applying a learned strategy to reach the goal

**Aggregate Scoring**
- Score = Sum of individual game scores ÷ Total number of games
- Final output: Percentage score between 0%-100%
- Scores are normalized per game to prevent any single game from dominating

**Source:** [ARC-AGI-3 technical research](https://arcprize.org/arc-agi/3)

### Human Testing Data

**Baseline Collection Details**
- Sample size: ~500 humans
- Duration: 90-minute sessions
- Location: San Francisco
- Population: Diverse, including unemployed/underemployed individuals
- Extended data: 1,200+ human players across 3,900+ games during preview period
- All human runs serve as the baseline every AI agent is scored against

**Human Performance Range**
- Typical baseline: 25-30%
- Most frontier models: Single-digit percentages
- Best preview models: 10-20% range
- Best preview submission (StochasticGoose): 12.58%

**Source:** [ARC-AGI-3: Understanding the New Benchmark](https://techplanet.today/post/arc-agi-3-understanding-the-new-benchmark-for-measuring-artificial-general-intelligence)

---

## 6. Evolution: ARC-AGI-1, 2, and 3

### ARC-AGI-1: The Original (2019)

**Introduction**
- Created by François Chollet, Google AI researcher and Keras founder
- Published in "On the Measure Of Intelligence"
- First comprehensive benchmark for general reasoning abilities

**Format**
- Grid-based reasoning puzzles
- Static, closed-world tasks
- Input/output pairs provided
- Typically 3 example I/O pairs per task
- 800 puzzle tasks total

**Challenge Type**
- Pattern recognition and abstraction
- Symbolic reasoning
- Rule inference from limited examples

**Source:** [The Evolving Landscape of AI Intelligence](https://medium.com/ai-simplified-in-plain-english/the-evolving-landscape-of-ai-intelligence-a-comparative-analysis-of-arc-agi-1-and-arc-agi-2-9e8782222c8d)

### ARC-AGI-2: Increased Complexity

**Enhancements**
- Preserved ARC format but sharply increased difficulty
- Deeper multi-step compositionality
- Richer symbolic interpretation required
- Context-dependent rule application
- Explicit resistance to brute-force search

**Key Innovation**
- Introduced "cost per task" as crucial metric
- Accurate intelligence requires both correctness AND efficiency
- Reflects real-world intelligence requirements

**Source:** [The Evolving Landscape of AI Intelligence](https://medium.com/ai-simplified-in-plain-english/the-evolving-landscape-of-ai-intelligence-a-comparative-analysis-of-arc-agi-1-and-arc-agi-2-9e8782222c8d)

### ARC-AGI-3: Interactive Paradigm Shift

**Revolutionary Changes**
- Moved from PASSIVE reasoning (solve given puzzles) to ACTIVE learning (explore unknown environments)
- Moved from static puzzles to dynamic interactive games
- Agents must discover game rules through experimentation
- No instructions, no descriptions, no winning conditions stated

**Game Mechanics**
- Turn-based games with internal logic to be discovered
- Progressive level complexity with new mechanics introduced
- 6 game environments with 8-10 levels each
- Thousands of total levels

**Key Capability Tested**
- Perception: What matters in visual environment
- Action selection: How to explore and learn
- Adaptation: Strategy adjustment without instructions
- World modeling: Building understanding from observations

**Performance Gap**
- Best AI in preview: 12.58% (vs. 100% human baseline)
- Frontier LLMs: Under 1%
- Top performer: CNN-based agent with structured exploration

**Source:** [ARC-AGI-3 Launches - AI Agents Must Learn, Not Memorize](https://awesomeagents.ai/news/arc-agi-3-interactive-benchmark/)

### Summary Table

| Aspect | ARC-AGI-1 | ARC-AGI-2 | ARC-AGI-3 |
|--------|-----------|-----------|-----------|
| **Format** | Static puzzles | Static puzzles | Interactive games |
| **Task Count** | 800 | Increased | 6 games, thousands of levels |
| **Interface** | I/O pairs | I/O pairs | Turn-based environment |
| **Learning Method** | Pattern matching | Abstraction | Active exploration |
| **Instructions** | Implicit in examples | Implicit in examples | None; discover rules |
| **Metric** | Accuracy | Accuracy + efficiency | Quadratic efficiency |
| **Intelligence Type** | Passive reasoning | Passive reasoning | Active learning & adaptation |

---

## 7. Preview Competition Results

### ARC-AGI-3 Preview Agent Competition

**Timeline**
- Dates: July 18 - August 19, 2025
- Partner: Hugging Face
- Type: Developer preview for agent development

**Winning Submission**
- **Team:** StochasticGoose @ Tufa Labs
- **Score:** 12.58% efficiency
- **Levels Completed:** 18 levels
- **Approach:** Convolutional Neural Network (CNN) with action-learning
- **Games Tested:** 3 private games

**Source:** [1st Place in the ARC-AGI-3 Agent Preview Competition](https://medium.com/@dries.epos/1st-place-in-the-arc-agi-3-agent-preview-competition-49263f6287db)

### Key Insights from Preview

**Performance Hierarchy**
- Frontier LLMs: Less than 1%
- Best AI performers: 10-20% range
- Winner (StochasticGoose): 12.58%
- Human baseline: 100%

**Winning Strategy Characteristics**
- CNN-based structured exploration outperformed GPT-5.x series by 12+ percentage points
- Graph-based exploration system (3rd place): Structured systematic exploration
- Non-LLM approaches dominated leaderboard
- Explicit state tracking and systematic exploration crucial

**What Didn't Work**
- Brute force approaches: Too inefficient for quadratic metric
- Pure language models: Struggled with visual learning and interactive control
- Random exploration: Poor action efficiency scores

**Breakthrough Insights**
- Interactive benchmarks are easy for humans but hard for AI
- Most humans beat games while AI struggled with efficiency
- Measuring information-to-strategy conversion reveals human-AI divide
- Some preview games too susceptible to random search
- Games refined for 2026 to resist brute force and better reflect true intelligence

**Source:** [ARC-AGI-3 Preview: 30-Day Learnings](https://arcprize.org/blog/arc-agi-3-preview-30-day-learnings)

---

## 8. Strategic Considerations for 2026

### Technical Requirements

**No Internet Access**
- All frontier model API calls are forbidden
- Models must be self-contained or run locally
- Pre-trained models must be bundled with submission
- LLM fine-tuning on offline data acceptable; API calls forbidden

**Execution Constraints**
- 12-hour time limit per submission
- Kaggle notebook environment
- One-click runnable requirement
- No manual intervention allowed

### Competitive Landscape Analysis

**Frontier LLMs Under-Perform**
- All frontier models score below 1% in preview
- Pure language model approaches insufficient
- Vision-language models still struggled significantly

**Winning Approaches**
- CNN-based agents with structured exploration
- Graph-based exploration systems
- Explicit state tracking and world modeling
- Combination of perception + systematic reasoning

**Key to Success**
- Action efficiency > success rate
- Exploration systematicity > exploration randomness
- Visual perception capabilities critical
- Ability to build and update world models essential

### Open Source Advantage

**Competition Philosophy**
- ARC Prize mission: Accelerate open-source AGI research
- Rewards sharing solutions freely with research community
- Open source requirement means:
  - Solutions available to all researchers immediately
  - Can't use proprietary closed-source techniques
  - Must be reproducible by others

**Practical Implications**
- Reproducibility crucial for verification and prize distribution
- Compute budget transparency required
- Cost-per-task metrics must be published
- Clever engineering matters as much as novel algorithms

---

## 9. Key Reference Resources

### Official Competition Pages
- [ARC Prize 2026 Main](https://arcprize.org/competitions/2026)
- [ARC-AGI-3 Competition Track](https://arcprize.org/competitions/2026/arc-agi-3)
- [ARC Prize Guide](https://arcprize.org/guide)
- [ARC Prize Verified Testing Policy](https://arcprize.org/policy)

### Documentation & Toolkit
- [ARC-AGI-3 Quickstart Documentation](https://docs.arcprize.org/)
- [ARC-AGI GitHub Repository](https://github.com/arcprize/ARC-AGI)
- [ARC-AGI-3 Agents Repository](https://github.com/arcprize/ARC-AGI-3-Agents)

### Kaggle Competitions
- [ARC Prize 2026 - ARC-AGI-3 Leaderboard](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3/leaderboard)
- [ARC Prize 2026 - ARC-AGI-2 Track](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2)
- [ARC Prize 2026 - Paper Track](https://www.kaggle.com/competitions/arc-prize-2026-paper-track)

### Leaderboards
- [Public ARC-AGI-3 Leaderboard](https://three.arcprize.org/leaderboard)
- [ARC Prize Leaderboard](https://arcprize.org/leaderboard)

### Technical Analysis & Research
- [ARC-AGI-3: Understanding the New Benchmark](https://techplanet.today/post/arc-agi-3-understanding-the-new-benchmark-for-measuring-artificial-general-intelligence)
- [Graph-Based Exploration for ARC-AGI-3](https://arxiv.org/abs/2512.24156)
- [1st Place Winner Analysis](https://medium.com/@dries.epos/1st-place-in-the-arc-agi-3-agent-preview-competition-49263f6287db)
- [ARC-AGI-3 Preview Learnings](https://arcprize.org/blog/aic-agi-3-preview-30-day-learnings)
- [Why Frontier Models Don't Generalize on ARC-AGI](https://labs.adaline.ai/p/what-is-the-arc-agi-benchmark-and)
- [ARC-AGI-3 Launch Announcement](https://awesomeagents.ai/news/arc-agi-3-interactive-benchmark/)

### Research Community
- [Awesome Agents](https://awesomeagents.ai/)
- [Hacker News Discussion](https://news.ycombinator.com/item?id=47521150)
- [AI Wiki - ARC-AGI-3](https://aiwiki.ai/wiki/ARC-AGI_3)

---

## 10. Competition Strategy Implications

### For Agent Development

1. **Vision-First Approach**
   - Strong CNN-based perception essential
   - 16-color discrete palette simplifies processing
   - 64×64 resolution manageable for standard architectures

2. **Structured Exploration**
   - Random exploration highly penalized by quadratic metric
   - Systematic state tracking and planning crucial
   - Graph-based approaches showed promise

3. **Action Efficiency**
   - Every action wasted costs quadratically
   - Minimize exploration-to-execution ratio
   - Build accurate world models quickly

4. **Multi-Game Generalization**
   - 6 different games with different mechanics
   - Must discover and adapt to new rule sets
   - Transfer learning from one game to others valuable

### For Competitive Success

1. **Open Source Quality**
   - Code must be production-ready and documented
   - Reproducibility = credibility = prizes
   - Consider educational value for research community

2. **Compute Efficiency**
   - 12-hour limit: efficient implementations matter
   - No GPU intensive requirements if possible
   - Pre-compute where feasible (without hardcoding)

3. **Offline First**
   - Design around zero-internet-access constraint from day one
   - Test in offline Kaggle environment early
   - No API fallbacks

4. **Documentation Excellence**
   - Clear explanation of approach
   - Cost-per-task metrics must be tracked
   - Reproducibility instructions crucial

---

**Document Last Updated:** March 26, 2026
**Research Compilation Source:** Comprehensive web search and official ARC Prize resources
