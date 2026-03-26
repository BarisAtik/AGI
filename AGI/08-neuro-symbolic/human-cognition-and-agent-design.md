# Human Cognition and Agent Design for ARC-AGI Reasoning Tasks

## Research Overview

This document synthesizes research on human performance on ARC (Abstraction and Reasoning Corpus) tasks and agent architecture design patterns for ARC-AGI-3 interactive reasoning benchmarks. The goal is to understand how humans solve abstract reasoning problems and translate those insights into effective AI agent designs.

---

## Part 1: Human Performance on ARC Tasks (H-ARC)

### Source
[H-ARC: A Robust Estimate of Human Performance on the Abstraction and Reasoning Corpus Benchmark](https://arxiv.org/html/2409.01374v1)

### Overview

H-ARC provides the first comprehensive, large-scale evaluation of human performance on the full ARC benchmark. Researchers evaluated 1,729 humans on all 400 training and 400 evaluation tasks from the original ARC dataset, collecting 15,744 total attempts with detailed behavioral traces.

### Key Human Performance Metrics

**Training Set Performance:**
- Empirical average: 76.2% correct
- Confidence interval: 73.3% - 77.2%

**Evaluation Set Performance:**
- Empirical average: 64.2% correct
- Confidence interval: 55.9% - 68.9%

**Task Solvability:**
- 790 out of 800 tasks (98.7%) were solved by at least one person in three attempts
- This indicates that nearly all publicly available ARC tasks are in principle solvable by typical crowd-workers

### Dataset Characteristics

The H-ARC dataset includes:
- Step-by-step action traces from the ARC user interface
- Natural-language solution descriptions (human-inferred rules/programs)
- Video recordings of human problem-solving behavior
- Behavioral data capturing how humans explore and reason

### Implications for Agent Design

1. **Achievable Performance Ceiling:** Agents targeting human-level reasoning should aim for 70-80% on training tasks and 55-70% on evaluation tasks.

2. **Task Variety:** The 64% evaluation set performance (vs 76% training) indicates significant generalization gaps between seen and novel tasks, suggesting agents need strong compositional reasoning and transfer learning capabilities.

3. **Solvability Spectrum:** Not all tasks are equally hard; understanding which task types humans find difficult can guide agent architecture development.

### Human Behavioral Insights

While not detailed in the summary, the action traces and solution descriptions in H-ARC provide insights into:
- How humans sample the problem space
- Which rules they hypothesize early vs. late
- Common failure modes and misconceptions
- Effective exploration strategies

---

## Part 2: ARC-AGI-3 Interactive Reasoning Benchmark

### Sources
- [ARC-AGI-3 Official Documentation](https://docs.arcprize.org/)
- [ARC-AGI-3 Overview](https://arcprize.org/arc-agi/3)
- [LangGraph Templates for ARC-AGI-3](https://www.joinplank.com/articles/arc-prize-langgraph)
- [Measuring Intelligence: ARC-AGI-3 is a Test For Agents](https://evoailabs.medium.com/measuring-intelligence-arc-agi-3-is-a-test-for-agents-0850e1531976)

### What Makes ARC-AGI-3 Different

Unlike static ARC tasks with fixed input-output examples, ARC-AGI-3 introduces **interactive game-like environments** where:

1. Agents must **infer task mechanics on-the-fly** through limited interactions
2. Agents must **adapt to increasing complexity** across levels within a game
3. Agents receive **sparse feedback** (rewards only on level completion)
4. Agents must **build adaptable world models** that generalize across novel game variants

### Game Environment Specifications

**Observation Space:**
- 64×64 grids with 16 possible colors
- Visual frames sent to agent on each step

**Action Space:**
- **RESET:** Restart the level/game if at the start
- **ACTION1-ACTION4:** Directional moves (up, down, left, right)
- **ACTION5:** General interaction (select, rotate, attach/detach, execute, etc.)
- **ACTION6:** Additional domain-specific action
- **UNDO:** (Unavailable during competition)

**Reward Signal:**
- Sparse: rewards only on level completion
- Games do not automatically reset on failure
- Agents must manage multiple attempts within a game

### Agent Interaction Loop

The canonical agent architecture follows this loop:

```
1. Receive observation frame (64x64 grid)
2. Process visual information with vision model
3. Maintain state representation (world model)
4. Select action based on exploration strategy
5. Execute action via API
6. Receive feedback (state change, reward signal)
7. Update internal state and hypotheses
8. Repeat until level completion or resource exhaustion
```

### Multi-Agent Graph Architecture (LangGraph Pattern)

The recommended template uses a multi-agent collaborative approach:

**Key Components:**
- **Memory Module:** Maintains game state history, tested actions, discovered rules
- **Vision Module:** Analyzes grid frames, detects changes, segments visual components
- **Planning Module:** Generates exploration strategies, prioritizes actions
- **Spatial Reasoning Module:** Understands geometric relationships, grid coordinates

**Advantages:**
- Stateful long-running execution (maintains memory across steps)
- Dynamic decision-making (agents collaborate and influence each other)
- Explicit reasoning traces (explainable action selection)
- Modular architecture (each capability can be specialized)

---

## Part 3: Exploration Strategies for Interactive Reasoning

### Source
[Graph-Based Exploration for ARC-AGI-3 Interactive Reasoning Tasks](https://arxiv.org/abs/2512.24156)

### Graph-Based Exploration Method (3rd Place Solution)

**Core Insight:** In sparse-feedback environments, explicit graph-structured state tracking substantially outperforms frontier LLMs.

**Method:**

1. **State-Space Representation:** Maintain a directed graph of explored states
   - Each node represents a unique observed game state
   - Edges represent tested action-outcome transitions

2. **State Tracking:**
   - Segment visual frames into meaningful components
   - Track which states have been visited
   - Record which actions have been tried from each state

3. **Action Prioritization:**
   - Prioritize actions based on visual salience (changes in frame regions)
   - Prefer untested state-action pairs
   - Use shortest-path analysis to reach unexplored states

4. **Systematic Exploration:**
   - Maintain exploration queue ordered by priority
   - Track previously attempted actions to avoid redundancy
   - Balance exploration breadth (new states) vs. depth (thorough state analysis)

**Performance:**
- Solves median 30 out of 52 levels across six games (57.7% success)
- Ranks 3rd on private leaderboard
- Substantially outperforms frontier LLM-based agents

**Key Finding:** This training-free approach demonstrates that explicit state tracking and systematic exploration are more effective than end-to-end learning for sparse-feedback interactive tasks.

### StochasticGoose: CNN-Based Action Learning (1st Place Solution)

**Source:** [1st Place in the ARC-AGI-3 Agent Preview Competition](https://medium.com/@dries.epos/1st-place-in-the-arc-agi-3-agent-preview-competition-49263f6287db)

**Agent Details:**
- Developer: Dries Smit (Tufa Labs)
- Architecture: Convolutional Neural Network (CNN)
- Achieved 12.58% score, 18 levels completed, most games completed

**Exploration Strategy:**

The key innovation is addressing the **massive action space problem:**
- ACTION5 (general interaction) produces 64×64 = 4,096 possible click coordinates
- Random exploration is prohibitively expensive

**Solution: Predict Which Actions Cause State Changes**

1. **CNN Prediction Model:** Train model to predict which actions (ACTION1-ACTION6) will result in new frame states
2. **Hierarchical Sampling:**
   - First layer: Select action type
   - Second layer: If action involves coordinates, sample coordinates via convolution (preserves 2D spatial bias)
3. **Efficiency Gain:** Only explore actions predicted to cause changes, dramatically reducing action space

**Technical Implementation:**
- Coordinate sampling done purely through convolution to maintain 2D grid structure
- Model trained on observed frame transitions
- Biases exploration toward actions with empirically high impact

**Performance Results:**
- Highest score in competition (12.58%)
- Most levels completed (18)
- Most games completed among all solutions
- Demonstrates that learned action selection substantially outperforms random exploration

---

## Part 4: Agent Architecture Frameworks

### ARCLE: Reinforcement Learning Environment

**Source:** [ARCLE: The Abstraction and Reasoning Corpus Learning Environment for Reinforcement Learning](https://arxiv.org/abs/2407.20806)

**Purpose:** Provide standardized RL environment for ARC-like tasks (Gymnasium-compatible)

**Environment Types:**

1. **O2ARCEnv:** Full embodied action/observation spaces following O2ARC interface
2. **ARCEnv:** Testing web interface
3. **RawARCEnv:** Restricted action space (color modifications, grid size changes only)

**Action Set:**
- Coloring specific pixels
- Moving pixels/regions
- Rotating objects
- Resizing grids
- Composition operations

**Training Results:**
- PPO agents with non-factorial policies achieved **95%+ success** in random settings
- 20-30% higher success rate in complex ARC tasks vs. baseline
- Demonstrates feasibility of RL approaches for abstract reasoning

**Relevance to ARC-AGI-3:**
While ARCLE targets classical ARC tasks rather than interactive games, it demonstrates how RL agents can learn effective grid manipulation strategies, informing design of ARC-AGI-3 agents.

---

## Part 5: Data Augmentation and Synthetic Task Generation

### Source: Procedural Generation for ARC

**Problem:** Limited number of ARC-AGI tasks (400 training) insufficient for training large models

**Solutions:**

#### Re-ARC (Reverse Engineering Approach)
- Uses Domain-Specific Language (DSL) to represent each task as combination of primitive functions
- Each task has hand-crafted procedural generator
- Generate unlimited samples by randomizing primitive parameters
- Created 400,000 synthetic ARC-like puzzles for pre-training

#### ARC-GEN (Google's Mimetic Generator)
- Procedural benchmark generator targeting exhaustive coverage of ARC-AGI-1 training tasks
- Matches original task distribution
- More scalable than hand-crafted generators

#### Traditional Data Augmentation
- Symmetry-based transformations (rotations, reflections)
- Traversal-driven modifications
- Cellular automata variations
- Color mapping permutations

**Test-Time Augmentation:**
- Generate small training datasets from augmented input-output pairs
- Remove individual examples and regenerate with transformations
- Apply rotation, reflection, color remapping
- Create ensemble of task variants

### ARC-TGI: Human-Validated Task Generators

**Source:** [ARC-TGI: Human-Validated Task Generators with Reasoning Chain Templates for ARC-AGI](https://arxiv.org/abs/2603.05099)

**Framework Design:**

Each generator module has three stages:

1. **Sample Inputs:** Randomize nuisance factors (grid size, colors, object positions)
2. **Apply Transformation:** Deterministic rule application (the latent task logic)
3. **Construct Episode:** Assemble train/test pairs under task-level constraints

**Key Innovation: Reasoning Chain Templates**

Each generated task is paired with:
- **Input Reasoning Chain:** Natural-language description of input grid contents
- **Transformation Reasoning Chain:** Solution steps as templates with variable slots
- Instantiated from sampled task parameters
- Provides solver-facing explanations aligned to each instance

**Constraint Enforcement:**

ARC-TGI enforces critical constraints:
- Prevent test-only features (all test variations must be inferable from training)
- Reject degenerate shortcuts (identity, constant outputs)
- Ensure training pairs collectively expose rule variations
- Validate grids and reasoning traces remain correct under sampling

**Human Validation Process:**

1. Contributors analyze tasks and author reasoning templates
2. LLM optionally drafts generator code
3. Iterative refinement under repeated sampling and visualization
4. Human review ensures naturalness and correctness

**Scale and Coverage:**

- **461 total generators** released
- **180 ARC-Mini tasks**
- **215 ARC-AGI-1 tasks** (200 train, 15 eval)
- **66 ARC-AGI-2 tasks** (55 train, 11 eval)

**Advantages:**

1. **Scalable Sampling:** Each generator defines distribution, not single task
2. **Dataset-Centric Analysis:** Enables diversity and distributional coverage studies
3. **Solver Supervision:** Reasoning chains provide training signal
4. **Human-Aligned:** Task constraints ensure human-solvable difficulty

---

## Synthesis: Designing ARC-AGI-3 Agents

### Architecture Patterns

**Pattern 1: Explicit State Graph + Vision**
- Maintain directed graph of explored states
- Use CNN/vision model for frame analysis
- Prioritize actions based on visual changes
- Results: Achieves 57.7% success without learned models

**Pattern 2: Learned Action Value Prediction**
- Train CNN to predict action impact (will this action change state?)
- Use predictions to bias exploration toward impactful actions
- Results: Achieves 12.58% score with most levels/games completed

**Pattern 3: Multi-Agent Collaboration (LangGraph)**
- Memory module for history tracking
- Vision module for frame understanding
- Planning module for strategy generation
- Spatial reasoning for grid relationships
- Results: Recommended template for interactive agents

### Key Insights from Human Performance

1. **Humans solve ~76% of training tasks:** Target agents should reach this level
2. **Humans solve ~64% of evaluation tasks:** Generalization gap shows importance of compositional reasoning
3. **Almost all tasks are solvable:** 98.7% of tasks were solved by at least one person
4. **Behavioral traces matter:** Understanding human action sequences can inform agent design

### Data Strategy

1. **Pre-train on synthetic tasks:** Use Re-ARC or ARC-GEN for initialization
2. **Use reasoning chain supervision:** ARC-TGI templates provide learning signal
3. **Apply test-time augmentation:** Generate task variants during evaluation
4. **Leverage human behavioral data:** H-ARC action traces inform exploration strategy

### Exploration Strategy Recommendations

**For Resource-Constrained Agents:**
- Implement explicit state graph tracking
- Use visual change detection for action prioritization
- Maintain exploration queue of untested state-action pairs
- This baseline achieves competitive results without learning

**For Learned Agents:**
- Train CNN to predict action impact on game state
- Use impact predictions to guide exploration
- Combine with hierarchical action sampling (action type → coordinates)
- This approach scales better with more interactions

**For Multi-Agent Frameworks:**
- Coordinate memory (shared state history)
- Vision-guided planning (visual features → action proposals)
- Spatial reasoning for grid-based action selection
- Explicit reasoning traces for interpretability

---

## Key References

### Human Performance
1. [H-ARC: A Robust Estimate of Human Performance on the Abstraction and Reasoning Corpus Benchmark](https://arxiv.org/abs/2409.01374)
2. [A Comprehensive Behavioral Dataset for the Abstraction and Reasoning Corpus](https://www.nature.com/articles/s41597-025-05687-1)

### Interactive Reasoning
3. [ARC-AGI-3 Official Documentation](https://docs.arcprize.org/)
4. [ARC-AGI-3 Benchmark Overview](https://arcprize.org/arc-agi/3)
5. [ARC-AGI-3 Preview: 30-Day Learnings](https://arcprize.org/blog/arc-agi-3-preview-30-day-learnings)

### Exploration Strategies
6. [Graph-Based Exploration for ARC-AGI-3 Interactive Reasoning Tasks](https://arxiv.org/abs/2512.24156)
7. [1st Place in the ARC-AGI-3 Agent Preview Competition](https://medium.com/@dries.epos/1st-place-in-the-arc-agi-3-agent-preview-competition-49263f6287db)
8. [3rd Place Solution: Explore It Till You Solve It](https://github.com/dolphin-in-a-coma/arc-agi-3-just-explore)

### Architecture Frameworks
9. [LangGraph Templates for ARC-AGI-3](https://www.joinplank.com/articles/arc-prize-langgraph)
10. [ARCLE: The Abstraction and Reasoning Corpus Learning Environment for Reinforcement Learning](https://arxiv.org/abs/2407.20806)
11. [GitHub: ARCLE Environment](https://github.com/ConfeitoHS/arcle)

### Data Augmentation and Task Generation
12. [ARC-TGI: Human-Validated Task Generators with Reasoning Chain Templates for ARC-AGI](https://arxiv.org/abs/2603.05099)
13. [ARC-GEN: A Mimetic Procedural Benchmark Generator](https://arxiv.org/abs/2511.00162)
14. [GitHub: ARC-GEN](https://github.com/google/ARC-GEN)
15. [ARC Prize Guide: Data Augmentation](https://arcprize.org/guide)

### Related Resources
16. [ARC Prize Official Website](https://arcprize.org/)
17. [GitHub: ARC-AGI](https://github.com/fchollet/ARC-AGI)
18. [Measuring Intelligence: ARC-AGI-3 is a Test For Agents](https://evoailabs.medium.com/measuring-intelligence-arc-agi-3-is-a-test-for-agents-0850e1531976)

