# ARC-AGI GitHub Repositories & Tools Inventory

**Last Updated:** 2026-03-26

---

## OFFICIAL REPOSITORIES

### 1. ARC-AGI-3-Agents (Official Template)

**GitHub:** [arcprize/ARC-AGI-3-Agents](https://github.com/arcprize/ARC-AGI-3-Agents)

**Purpose:** Official agent template for the ARC-AGI-3 competition. Provides a structured framework for developing AI agents that can solve interactive, turn-based 2D grid games.

**Approach:**
- API-based system for game execution and replay tracking
- Local environment execution via ARC-AGI toolkit
- Standardized agent interfaces with consistent action/observation patterns
- Frame-based feedback system with game state, available actions, and completion metrics

**Key Features:**
- Pre-built random agent example demonstrating basic interaction
- Support for multiple game environments (e.g., ls20)
- Python-based framework with dependency management via `uv`
- Pytest testing infrastructure for agent validation
- Pre-commit hooks with Ruff for code quality
- Optional observability through AgentOps integration
- AgentOps observability platform for real-time monitoring and debugging

**Language:** Python

**How We Could Use It:**
- Starting point for building custom agents for ARC-AGI-3
- Reference implementation for understanding agent-environment interaction patterns
- Template for rapid experimentation with different agent architectures
- Baseline for comparing novel approaches

---

### 2. ARC-AGI-2 Dataset

**GitHub:** [arcprize/ARC-AGI-2](https://github.com/arcprize/ARC-AGI-2)

**Purpose:** Official dataset repository for ARC-AGI-2. Contains the core benchmark tasks and associated tools.

**Dataset Contents:**
- **1,000 public training tasks** — demonstrate task format and Core Knowledge priors used by ARC-AGI
- **120 public evaluation tasks** — for testing models that have never seen them before

**Data Structure:**
- Tasks stored in JSON format
- `data/training/` folder: 1,000 training tasks (combines ARC-AGI-1 + new tasks)
- `data/evaluation/` folder: 120 evaluation tasks
- Each task JSON contains: "train" (demonstration input/output pairs)

**Description:** "ARC can be seen as a general artificial intelligence benchmark, as a program synthesis benchmark, or as a psychometric intelligence test. It is targeted at both humans and artificially intelligent systems that aim at emulating a human-like form of general fluid intelligence."

**How We Could Use It:**
- Direct access to training and evaluation benchmarks
- Understanding task structure and format for custom solvers
- Baseline for evaluating solution approaches
- Resource for analysis of problem types and complexity distribution

---

### 3. ARC-AGI-3-Benchmarking

**GitHub:** [arcprize/arc-agi-3-benchmarking](https://github.com/arcprize/arc-agi-3-benchmarking/)

**Purpose:** Official benchmarking suite for testing AI models and agents on ARC-AGI-3 environments.

**Key Features:**
- Model configuration via YAML entries (model name, provider, pricing, API parameters)
- Scorecard management with results saved to ARC server
- Scorecards viewable at `three.arcprize.org/scorecards` (when logged in)
- Systematic evaluation of multiple LLMs against ARC-AGI-3 benchmark

**What is ARC-AGI-3:**
Interactive reasoning benchmark that challenges AI agents to:
- Explore novel environments
- Acquire goals on the fly
- Build adaptable world models
- Learn continuously from experience

**How We Could Use It:**
- Evaluate custom agent performance against official benchmarks
- Compare multiple model/agent configurations systematically
- Track performance metrics and create comparative scorecards
- Integrate custom models into benchmarking framework

---

## TOP SOLUTIONS

### 4. StochasticGoose (1st Place ARC-AGI-3)

**GitHub:** [DriesSmit/ARC3-solution](https://github.com/DriesSmit/ARC3-solution)

**Achievement:** **1st Place** in ARC-AGI-3 Agent Preview Competition

**Approach:** Action-learning agent using reinforcement learning to predict which actions cause frame changes.

**Architecture:**
- CNN-based model predicting action outcomes (ACTION1-ACTION6)
- Focuses on actions that result in new frame states
- More efficient exploration than random selection
- Learns action-environment relationships through experience

**Key Features:**
- Simple but effective reinforcement learning strategy
- Frame change detection for action evaluation
- Generalizes to entirely new games not seen during development
- Developed at Tufa Labs

**Language:** Python

**How We Could Use It:**
- Reference implementation for RL-based agent design
- Proven approach for action learning in unknown environments
- Insights into what makes agents effective on ARC-AGI-3
- Starting point for improving upon winning methodology

---

### 5. NVARC (1st Place ARC Prize 2025 - Kaggle Leaderboard)

**GitHub:** [1ytic/NVARC](https://github.com/1ytic/NVARC)

**Achievement:** **1st place on Kaggle ARC Prize 2025 public leaderboard** with 27.64% score

**Team:** Ivan Sorokin and Jean-Francois Puget (NVIDIA Kaggle Grandmasters)

**Approach:** Multi-component ensemble combining synthetic data generation, fine-tuned language models, and recursive pattern matching.

**Architecture:**

**1. Synthetic Data Generation Pipeline (SDG)**
- 103,000 synthetic puzzles generated
- 3.2 million augmented puzzle variants
- Concept decomposition and staged puzzle generation
- Generated text artifacts for training

**2. ARChitects (Qwen3 Fine-tuning)**
- Fine-tuned Qwen3 4B language model
- Uses LoRA (Low-Rank Adaptation) techniques
- Outperforms far larger models (20 cents per task)
- Scripts and hyperparameters in ARChitects folder

**3. Tiny Recursive Models (TRM)**
- Improved recursive modeling for pattern recognition
- Integration with broader ensemble approach
- Training procedures documented in TRM folder

**Cost Efficiency:** $0.20 per task (significantly cheaper than frontier models)

**Languages:** Python

**How We Could Use It:**
- Understand synthetic data generation at scale for ARC-like puzzles
- Learn LoRA fine-tuning techniques for efficient model adaptation
- Implement multi-model ensemble approaches
- Leverage publicly available synthetic puzzle dataset (103k examples)
- Cost-effective baseline approach for production systems

---

### 6. Poetiq ARC-AGI Solver

**GitHub:** [poetiq-ai/poetiq-arc-agi-solver](https://github.com/poetiq-ai/poetiq-arc-agi-solver)

**Achievement:** Record-breaking submission to ARC-AGI-1 and ARC-AGI-2 benchmarks. Top of official leaderboard per follow-up post: "Poetiq Shatters ARC-AGI-2 State of the Art at Half the Cost"

**Approach:** LLM-based solution for automated puzzle solving with cost optimization.

**Key Features:**
- API-based integration for multiple LLM providers
- Configuration via `.env` file with API keys
- Reproducible results with documented parameters
- Performance tracking and result management
- Usage: Create `.env` with API keys, modify `main.py` for problem set selection

**How We Could Use It:**
- Reference for state-of-the-art performance metrics
- Understanding cost-optimized approaches to ARC solving
- LLM integration patterns and API management
- Baseline for evaluating new approaches

---

### 7. epang080516 SoTA Solution (77.1% on ARC-AGI-1)

**GitHub:** [epang080516/arc_agi](https://github.com/epang080516/arc_agi)

**Achievement:**
- **77.1% on ARC-AGI-1** (beats frontier models)
- **26.0% on ARC-AGI-2**

**Approach:** DreamCoder-inspired, LLM-assisted program synthesis with learned concept libraries.

**Architecture:**

**Library-Based Program Synthesis:**
- Maintains dynamically growing library of reusable programs
- Starts from empty library, expands as tasks are solved
- Programs are Python code (Turing-complete)
- Grows system expertise by adding promising programs to library

**Selection & Iteration:**
- Score-weighted program selection using softmax probabilities
- Ranks programs by: primary accuracy (correct examples) + secondary accuracy (cell-level correctness)
- Balances exploitation/exploration by occasionally selecting non-optimal programs
- Multi-round iteration: initial training on 1,000 tasks, then 2 additional rounds with 5 programs per task

**Key Advantage:**
Transfers learned concepts across tasks—avoids inefficiency of treating each puzzle independently.

**Cost Efficiency:**
- $2.56 per task (vs competitors' $29-$400)
- Best performance-cost metric; breaks existing Pareto frontier

**Language:** Python

**How We Could Use It:**
- Learn program synthesis approach with concept transfer
- Implement cost-efficient solving strategies
- Understand library-based reasoning systems
- Build on DreamCoder methodology for novel abstractions

---

### 8. SakanaAI Multi-LLM AB-MCTS for ARC-AGI-2

**GitHub:** [SakanaAI/ab-mcts-arc2](https://github.com/SakanaAI/ab-mcts-arc2)

**Purpose:** Implementation of Multi-LLM AB-MCTS (Adaptive Branching Monte Carlo Tree Search) for solving ARC-AGI-2 using multiple frontier LLMs working together.

**Approach:** Inference-time scaling through collective intelligence and trial-and-error exploration.

**Architecture:**

**Algorithm:** AB-MCTS (Adaptive Branching Monte Carlo Tree Search)
- Enables trial-and-error efficiently
- Allows different AIs to think collectively
- Supports inference-time scaling

**Multi-LLM Ensemble:**
- Combines three frontier models:
  - OpenAI o4-mini
  - Google Gemini 2.5 Pro
  - DeepSeek R1-0528
- Over 100 trial-and-error rounds
- Results exceed single-model performance (o4-mini alone)

**Implementation:**
- Powered by TreeQuest library for flexible tree search API
- Supports custom model integration
- Handles multi-model coordination during inference

**Languages:** Python

**How We Could Use It:**
- Implement multi-model ensemble strategies
- Learn inference-time scaling techniques
- Build adaptive tree search systems for complex reasoning
- Coordinate multiple AI systems toward common solutions
- Research collective intelligence in AI

---

## KEY TOOLS

### 9. ARC-DSL: Domain Specific Language

**GitHub:** [michaelhodel/arc-dsl](https://github.com/michaelhodel/arc-dsl)

**Purpose:** Domain Specific Language designed to be expressive enough to solve arbitrary ARC tasks using only few primitives.

**Approach:**
- Minimalist primitive set, each useful for many tasks
- Focuses on expressiveness with minimal complexity
- Custom solver programs written in the DSL for training tasks

**Key Features:**
- Well-documented writeup in `arc_dsl_writeup.pdf`
- Example generators written as standalone Python functions
- Median generator: ~40 lines of code using 22 DSL primitive calls
- Focus on improving search efficiency through appropriate language design

**Why It Matters:**
"A good DSL can greatly improve search efficiency, given it is what we search over. One challenge with most DSLs is that they are hand-coded, with the author solving all the ARC training tasks and then producing a set of language primitives necessary to solve all the problems they have seen."

**Language:** Python with DSL

**How We Could Use It:**
- Foundation for building custom DSLs for specific problem classes
- Understand design principles for programming languages targeting ARC
- Leverage existing DSL for hypothesis generation
- Learn search efficiency optimization techniques
- Reference for hand-coding domain languages

---

### 10. RE-ARC: Reverse Engineering ARC

**GitHub:** [michaelhodel/re-arc](https://github.com/michaelhodel/re-arc)

**Purpose:** Procedurally generate examples for ARC training tasks by reverse-engineering the underlying transformation logic.

**Approach:**
- Analyzes original task examples to infer underlying distribution
- Implements task-specific example generators based on inferred rules
- Generates additional valid examples by sampling from learned distribution
- Validates generated examples using task solver programs

**Key Features:**
- **1,000 verified generated examples** for each of the 400 training tasks
- Difficulty metrics for each example
- Task-level metadata (runtime, sample-efficiency)
- Files:
  - `generators.py`: Task-specific example generators
  - `verifiers.py`: Task solver programs for validation
- Available as `re_arc.zip` with full dataset

**Significance:**
Reverse-engineered the assumed underlying distribution of examples for each task, enabling efficient sampling from learned task distributions.

**Language:** Python

**How We Could Use It:**
- Access 400,000 verified synthetic examples (1,000 per task)
- Understand task transformation logic through generators
- Train models on augmented datasets
- Learn example generation and validation techniques
- Improve task understanding through reverse engineering

---

### 11. ARC-GEN: Procedural Benchmark Generator

**GitHub:** [google/ARC-GEN](https://github.com/google/ARC-GEN)

**Purpose:** Mimetic procedural benchmark generator for the Abstraction and Reasoning Corpus.

**Approach:**
- Procedurally generates synthetic examples matching original task distributions
- Covers all 400 ARC tasks with validated generators
- Enables customization and variation on individual tasks

**Key Features:**
- **100,000 pre-generated examples** available on Kaggle (covering all 400 tasks)
- Command-based interface: `generate [task_number] [num_examples]`
- Validation support: Ensures generators collectively reproduce original ARC-AGI-1 suite
- All 400 generators pass validation
- Supports customized variations on individual tasks

**Available Data:**
- Pre-generated dataset of 100,000 examples on Kaggle
- Fully customizable generation via Python

**Language:** Python

**How We Could Use It:**
- Generate unlimited synthetic training examples for any ARC task
- Augment training datasets for model development
- Validate generator implementations against original tasks
- Create task-specific variations for specialized training
- Research data augmentation strategies

---

### 12. ARCKit: Tools for ARC Datasets

**GitHub:** [mxbi/arckit](https://github.com/mxbi/arckit)

**Purpose:** Comprehensive Python and command-line tools for easily working with ARC, ARC-AGI, and ARC-AGI-2 datasets.

**Key Features:**
- Load data in friendly format without separate download
- Support for multiple dataset versions
- Vector graphics visualization via `arckit.vis` submodule using `drawsvg`
- PyPI package for easy installation: `pip install arckit`

**Supported Datasets:**
- Latest ARC-AGI-2 (default)
- ARC-AGI (`kaggle/kaggle2024`)
- 2025 Kaggle competition dataset (`kaggle/kaggle2025`)
- Original ARC from 2019 Kaggle competition (`arc/kaggle2019`)

**License:** Apache 2.0 (same as underlying ARC/ARC-AGI-2 datasets)

**Maintainer:** Mikel Bober-Irizar

**Language:** Python

**How We Could Use It:**
- Quick data loading without manual downloads
- Standardized data handling across projects
- Create visualizations of tasks and solutions
- Switch between different ARC dataset versions easily
- Build tools on top of standardized data interface
- Integrate into analysis and evaluation pipelines

---

## STRATEGIC SUMMARY

### By Use Case:

**For Building Agents:**
- Start: [ARC-AGI-3-Agents](#1-arc-agi-3-agents-official-template)
- Reference: [StochasticGoose](#4-stochasticgoose-1st-place-arc-agi-3)
- Benchmark: [arc-agi-3-benchmarking](#3-arc-agi-3-benchmarking)

**For Training Models:**
- Data: [ARC-AGI-2 Dataset](#2-arc-agi-2-dataset), [RE-ARC](#10-re-arc-reverse-engineering-arc), [ARC-GEN](#11-arc-gen-procedural-benchmark-generator)
- Tools: [ARCKit](#12-arckit-tools-for-arc-datasets)
- Approaches: [NVARC](#5-nvarc-1st-place-arc-prize-2025---kaggle-leaderboard) (synthetic data), [epang080516](#7-epang080516-sota-solution-771-on-arc-agi-1) (program synthesis)

**For Advanced Research:**
- Multi-Model Systems: [SakanaAI AB-MCTS](#8-sakanaai-multi-llm-ab-mcts-for-arc-agi-2)
- Language Design: [ARC-DSL](#9-arc-dsl-domain-specific-language)
- Task Analysis: [RE-ARC](#10-re-arc-reverse-engineering-arc)

**For Production Systems:**
- Cost-Optimized: [NVARC](#5-nvarc-1st-place-arc-prize-2025---kaggle-leaderboard) ($0.20/task), [epang080516](#7-epang080516-sota-solution-771-on-arc-agi-1) ($2.56/task)
- SOTA Performance: [Poetiq](#6-poetiq-arc-agi-solver), [SakanaAI](#8-sakanaai-multi-llm-ab-mcts-for-arc-agi-2)

---

## PERFORMANCE BENCHMARKS

| Solution | ARC-AGI-1 | ARC-AGI-2 | Cost/Task | Approach |
|----------|-----------|-----------|-----------|----------|
| epang080516 | **77.1%** | 26.0% | $2.56 | Program synthesis + library |
| NVARC | — | 27.64% | $0.20 | Synthetic data + fine-tuned 4B model |
| StochasticGoose | — | — | — | RL action learning (ARC-AGI-3) |
| Poetiq | — | Top leaderboard | — | LLM-based (record-breaking) |
| SakanaAI AB-MCTS | — | Strong | — | Multi-LLM inference-time scaling |

---

## DATASET STATISTICS

- **ARC-AGI-1:** 400 tasks (training)
- **ARC-AGI-2:** 1,000 training + 120 evaluation tasks
- **RE-ARC Generated:** 400,000 verified examples (1,000 per ARC-AGI-1 task)
- **ARC-GEN Generated:** 100,000+ examples (all 400 ARC-AGI-1 tasks)
- **NVARC Synthetic:** 103,000 synthetic puzzles + 3.2M augmented variants

---

## TOOLS & INFRASTRUCTURE

- **Language:** Predominantly Python
- **Data Formats:** JSON (tasks), Kaggle datasets
- **Integration Points:**
  - Kaggle (NVARC, ARC-GEN datasets)
  - GitHub (all repositories)
  - HuggingFace (human testing dataset: `arcprize/arc_agi_2_human_testing`)
- **Development Patterns:**
  - API keys via `.env` files
  - Configuration via YAML (benchmarking)
  - pytest for testing
  - Virtual environments recommended

---

## REFERENCES & LINKS

- **Official ARC Prize:** https://arcprize.org/
- **ARC-AGI-3 Documentation:** https://docs.arcprize.org/
- **ARC Prize Foundation GitHub:** https://github.com/arcprize
- **Medium Article (1st Place ARC-AGI-3):** https://medium.com/@dries.epos/1st-place-in-the-arc-agi-3-agent-preview-competition-49263f6287db
- **NVIDIA Blog (NVARC):** https://developer.nvidia.com/blog/nvidia-kaggle-grandmasters-win-artificial-general-intelligence-competition/
- **Sakana AI AB-MCTS:** https://sakana.ai/ab-mcts/
- **Substack (epang080516 SoTA):** https://ctpang.substack.com/p/arc-agi-2-sota-efficient-evolutionary
- **Kaggle (NVARC writeup):** https://www.kaggle.com/competitions/arc-prize-2025/writeups/nvarc
