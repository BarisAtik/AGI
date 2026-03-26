# ARC-AGI Foundational Papers: Comprehensive Research Notes

## Document Overview
This document synthesizes key insights from three foundational papers on ARC-AGI for competition strategy. Each section covers the paper's thesis, technical details, core knowledge priors, and practical implications for solver development.

---

## 1. ARC-AGI-2: A New Challenge for Frontier AI Reasoning Systems

**Paper Source:** [https://arxiv.org/html/2505.11831v2](https://arxiv.org/html/2505.11831v2)

**Authors:** François Chollet et al.

**Publication:** 2025

### Key Thesis & Contribution

ARC-AGI-2 represents a significant evolution of the original ARC-AGI benchmark, designed to challenge frontier AI systems with deeper compositional generalization requirements. The benchmark maintains the original core knowledge priors while substantially increasing task complexity through larger grids, more objects, more concepts per task, and emphasis on multi-rule compositional reasoning.

### Benchmark Structure

#### Test Sets & Calibration

- **Total Tasks:** 1,360 tasks (1,000 training + 360 evaluation)
- **Evaluation Sets:**
  - Public Evaluation: 120 tasks
  - Semi-Private Evaluation: 120 tasks (held on Kaggle for intra-year competition)
  - Private Evaluation: 120 tasks (held on Kaggle for leaderboard)

#### Calibration Methodology

- **Human Validation:** 400+ participants from general public tested on 1,417 unique candidate tasks
- **Success Criterion:** Minimum of "two people in two attempts or less" per task
- **Average Solving Time:** ~2.3 minutes per task
- **Distribution Matching:** Eval sets are statistically similar with <1 percentage point expected score difference across sets
- **Test Coverage:** Each task attempted by approximately 9-10 participants on average
- **Expert Performance:** 100% solve rate by expert panels; 60% by average individual test-takers; ~75% by those who attempt each task

### Difficulty Levels & Task Complexity Factors

#### Increase from ARC-AGI-1 to ARC-AGI-2

1. **Novelty:** Every task is entirely novel (no overlap with original benchmark)
2. **Information Content:** Tasks feature:
   - Larger grids
   - More objects per grid
   - More concepts per task
   - Greater compositional complexity

3. **Complexity Characteristics:**
   - Tasks designed to minimize susceptibility to brute-force program search
   - Wider range of difficulty to measure capability gaps
   - Emphasis on human-scale solvability while challenging AI systems

### Core Task Categories

#### 1. Multi-Rule Compositional Reasoning
- Tasks requiring simultaneous application of multiple rules
- Rules that interact with each other
- Current systems struggle when rules must be composed together

#### 2. Multi-Step Compositional Reasoning
- Sequential application of multiple compositional rules
- Tasks are on average larger in size
- Involve greater number of colors
- Require procedural composition of learned rules

#### 3. Contextual Rule Application
- Rules must be applied differently based on context
- Systems tend to fixate on superficial patterns
- Require understanding underlying selection principles
- Challenge: distinguishing context-dependent vs. context-invariant rules

#### 4. Symbolic Interpretation
- Symbols must be interpreted as having meaning beyond visual patterns
- Current systems check symmetry, mirroring, and transformations but fail to assign semantic significance
- Requires meta-level reasoning about symbol semantics

#### 5. In-Context Symbol Definition
- Symbols defined within task context
- Requires learning symbol meaning from limited examples
- Systems must generalize symbolic definitions across grid transformations

### Evaluation Methodology

#### Design Principles
- Tasks designed based on AI capability studies to specifically challenge:
  - Symbolic interpretation
  - Compositional reasoning
  - Contextual rule application
  - Symbol definition and generalization

#### Performance Measurement
- Comparable scoring across Public/Semi-Private/Private sets
- Assumes no overfitting; calibration ensures reliability
- Semi-Private set used for intra-year competition standings
- Private set used for official leaderboard rankings

#### Key Design Goals
1. Minimize susceptibility to naive or brute-force search
2. Provide wider useful range of scores
3. Measure gap in capabilities required to reach AGI
4. Isolate specific capability dimensions (vs. ARC-AGI-3 which includes interaction requirements)

### Core Knowledge Priors (Inherited from ARC-AGI-1)

ARC-AGI-2 maintains the four fundamental core knowledge priors defined in Chollet's original work:

1. **Objectness & Elementary Physics**
   - Object cohesion and persistence
   - Influence via contact
   - Spatial continuity

2. **Agentness & Goal-Directedness**
   - Recognition of intentional agents
   - Understanding goal-directed behavior
   - Agent-object interactions

3. **Natural Numbers & Elementary Arithmetic**
   - Basic numerical knowledge
   - Counting principles
   - Simple arithmetic operations

4. **Elementary Geometry & Topology**
   - Spatial relationships
   - Basic geometric principles
   - Topological properties (connectivity, boundaries)

### Technical Details for Solver Development

#### Task Characteristics
- Grid-based visual reasoning problems
- Input/output demonstration format
- Requires learning transformation rules from examples
- Average task difficulty calibrated for 60% human solve rate
- Compositional generalization emphasized over individual skill

#### Challenge Areas for Current Systems
1. **Compositional Generalization:** Limited ability to combine known rules in novel ways
2. **Contextual Reasoning:** Difficulty applying rules conditionally based on context
3. **Symbolic Semantics:** Struggle to assign meaning to symbols beyond visual patterns
4. **Multi-Step Reasoning:** Difficulty maintaining and sequencing multiple transformation rules

### Implications for Competition Strategy

- **Compositional Architecture:** Solver must support composing learned rule components
- **Context Awareness:** Design for conditional rule application based on input context
- **Semantic Reasoning:** Implement symbol interpretation beyond pattern matching
- **Test-Time Adaptation:** Consider multi-step refinement during inference
- **Scale vs. Algorithm:** Parameter efficiency (7M-76K parameters seen competitive performance) suggests algorithmic innovation more valuable than scale

---

## 2. On the Measure of Intelligence by François Chollet

**Paper Source:** [https://arxiv.org/abs/1911.01547](https://arxiv.org/abs/1911.01547)

**Author:** François Chollet (Google, Inc.)

**Publication:** 2019

**Alternative Resources:**
- [ArXiv HTML Version](https://arxiv.org/html/1911.01547v2)
- [Paper Summary](https://liamwellacott.github.io/artificial%20intelligence/on-the-measure-of-intelligence/) (Liam Wellacott)
- [Academic Analysis](https://roberttlange.com/posts/2020/02/on-the-measure-of-intelligence/) (Robert Tlange)

### Key Thesis & Contribution

Chollet articulates a formal definition of intelligence based on Algorithmic Information Theory, arguing that intelligence is not skill at a specific task but rather the efficiency of skill acquisition across a scope of tasks. The paper establishes that measuring skill alone is insufficient for measuring intelligence because skill is heavily modulated by prior knowledge and experience.

### Definition of Intelligence

**Formal Definition:**

Intelligence is a measure of skill-acquisition efficiency over a scope of tasks, with respect to:
- **Priors:** Domain-specific knowledge and architectural biases
- **Experience:** Training data and accumulated learning
- **Generalization Difficulty:** Complexity of the task distribution

**Key Insight:** Unlimited priors or unlimited training data allow experimenters to "buy" arbitrary levels of skill, masking the system's actual generalization power.

**Critical Distinction:** Intelligence ≠ Skill
- Skill can be artificially inflated through task-specific training
- Intelligence measures how efficiently a system learns new skills with minimal priors and experience

### Why ARC-AGI Was Created

The paper motivated the creation of ARC (Abstraction and Reasoning Corpus) to address the shortcomings of existing benchmarks in measuring true intelligence rather than task-specific skill acquisition.

**Problems with Existing Approaches:**
1. Measuring skill alone masks generalization capability
2. Task-specific training data inflates apparent performance
3. No principled measure of skill-acquisition efficiency
4. Need for benchmark based on universal human priors

**Solution:** Build ARC on explicit core knowledge priors close to innate human cognitive capabilities.

### Core Knowledge Priors

Chollet identifies four fundamental categories of innate human knowledge based on Core Knowledge theory—cognitive building blocks either present at birth or acquired very early with minimal explicit instruction:

#### 1. Objectness & Elementary Physics
- **Definition:** Understanding objects as cohesive, persistent entities
- **Components:**
  - Object cohesion: Objects maintain spatial and temporal continuity
  - Object persistence: Objects continue to exist when not visible
  - Influence via contact: Objects affect each other through direct physical contact
  - Solidity: Objects cannot pass through each other

- **Implications for Solvers:**
  - Recognize connected components as single objects
  - Track object identity across transformations
  - Understand collision and contact dynamics

#### 2. Agentness & Goal-Directedness
- **Definition:** Recognizing intentional agents and understanding goal-directed behavior
- **Components:**
  - Agent identification: Distinguish agents from passive objects
  - Intentionality: Understand behavior as goal-directed
  - Agent-object interaction: Agents act upon objects to achieve goals
  - Action understanding: Infer goals from observed actions

- **Implications for Solvers:**
  - Identify actors vs. passive elements
  - Infer implicit goals or objectives from behavior patterns
  - Understand causal chains of intentional action

#### 3. Natural Numbers & Elementary Arithmetic
- **Definition:** Basic numerical knowledge and counting principles
- **Components:**
  - Counting: Ability to enumerate discrete objects
  - Number conservation: Quantity invariance under transformations
  - Subitizing: Immediate recognition of small quantities (3-4 items)
  - Basic arithmetic: Addition, subtraction, ordering
  - Cardinality: Understanding sets and their sizes

- **Implications for Solvers:**
  - Count objects and track quantity changes
  - Recognize numerical patterns and sequences
  - Apply arithmetic operations to grid transformations

#### 4. Elementary Geometry & Topology
- **Definition:** Understanding spatial relationships and geometric principles
- **Components:**
  - Spatial relationships: Position, distance, direction (above, below, left, right)
  - Geometric shapes: Recognition of basic forms (lines, rectangles, circles)
  - Topological properties:
    - Connectivity: Which elements are connected
    - Boundaries: Interior vs. exterior
    - Continuity: Paths and connectivity changes
    - Symmetry: Reflection and rotation invariance
  - Transformations: Translation, rotation, scaling, reflection

- **Implications for Solvers:**
  - Recognize geometric patterns and transformations
  - Understand connectivity and topology
  - Track spatial relationships and transformations

### Skill vs. Generalization

#### The Skill-Generalization Gap

**Problem:** Skill can be inflated artificially, masking poor generalization.

**Example:**
- A model memorizing specific patterns in training data achieves high skill on that task
- Same model fails completely on novel tasks (poor generalization)
- Traditional metrics credit the skill, ignoring the lack of intelligence

**Solution in ARC:**
- Minimal training examples (typically 2-5 input-output pairs)
- Novel evaluation tasks never seen during training
- Emphasis on transfer learning and compositional reasoning

#### Generalization Efficiency
- True intelligence measures how well systems learn from minimal experience
- Evaluated by performance on truly novel tasks
- Accounts for both ease of learning (low sample complexity) and breadth of learning (scope of tasks)

### Intelligence as Compression

**Core Insight:** Intelligence is fundamentally about conceptual compression—finding compact representations that capture the essence of problems.

**Implications:**
- Humans solve ARC tasks through high-level abstraction and conceptualization
- Pattern recognition and symbolic reasoning enable compact mental models
- Generalization stems from discovering underlying principles, not memorizing surface patterns

---

## 3. The ARC of Progress towards AGI: A Living Survey of Abstraction and Reasoning

**Paper Source:** [https://arxiv.org/html/2603.13372v1](https://arxiv.org/html/2603.13372v1)

**Survey Scope:** 82 approaches across three benchmark generations

**Coverage:** 65 papers with rigorous standardized test set evaluations

**Time Period:** Analysis through December 2025

### Key Thesis & Contribution

This comprehensive survey provides the first cross-generation analysis of approaches to ARC-AGI, revealing patterns of what works, what doesn't, and the fundamental capabilities gaps between current systems and AGI. The survey demonstrates that hybrid neural-symbolic approaches have become dominant, and that algorithmic innovation drives progress more than parameter scaling.

### Benchmark Evolution Across Generations

#### Three Benchmark Generations

All generations employ identical core knowledge priors and presentation formats, varying in task complexity and interaction requirements:

1. **ARC-AGI (Generation 1)**
   - Baseline challenge for abstract reasoning
   - Grid-based visual reasoning problems
   - Input-output demonstration format

2. **ARC-AGI-2 (Generation 2)**
   - Increased compositional complexity
   - Larger grids, more objects, more concepts
   - Deeper compositional generalization emphasis
   - Multi-rule and multi-step reasoning

3. **ARC-AGI-3 (Generation 3)**
   - Includes interactive elements
   - Isolates capability dimensions not covered by static tasks
   - Tests real-time reasoning and user interaction

#### Design Philosophy

By isolating specific capability dimensions across generations, the survey reveals:
- Which aspects of abstract reasoning current systems have mastered
- Which remain fundamentally challenging
- How architectural choices affect performance across different reasoning types

### Taxonomy of Approaches

#### Classification Framework

Approaches are taxonomized by their underlying methodology:

1. **Pure Neural Approaches**
2. **Pure Symbolic Approaches**
3. **Hybrid Neural-Symbolic Approaches**
4. **Other Specialized Approaches**

### Which Approaches Work Best

#### Overall Dominance Pattern

**Hybrid approaches dominate**, reflecting collective recognition that:
- Pure neural methods have consistent 20% ceiling on ARC-AGI performance
- Pure symbolic methods struggle with perception and induction
- Combination provides capabilities beyond either paradigm alone

#### Performance Breakdown

**Pure Neural Approaches:**
- Ceiling: ~20% on ARC-AGI-1
- Recent improvements with large language models, but fundamental limitations remain
- Effective at: Pattern recognition, perceptual tasks
- Weak at: Logical reasoning, compositional generalization, novel rule learning

**Pure Symbolic Approaches:**
- Variable performance (5-30% range)
- Effective at: Logical inference, rule application
- Weak at: Perception, noise handling, flexible induction
- Struggle with: Converting visual inputs to meaningful symbolic representations

**Hybrid Neural-Symbolic Approaches:**
- Best overall performance on ARC-AGI benchmark
- Combine neural perception with symbolic reasoning
- Most competitive submissions use this approach
- Performance range: 30-45% on ARC-AGI-1, lower on ARC-AGI-2

#### Key Finding: Parameter Efficiency

**Critical Discovery:** Competitive performance does not require massive scale.

**Examples of Efficient Models:**

1. **Tiny Recursive Model (TRM)**
   - Parameters: 7 million
   - ARC-AGI-1 Performance: 45% test accuracy
   - ARC-AGI-2 Performance: 8% test accuracy
   - Key insight: Most task-specific training happens at test-time

2. **CompressARC**
   - Parameters: 76,000 (!)
   - Demonstrates extreme parameter efficiency
   - Uses compression-based reasoning principles

**Implication:** Algorithmic innovation and test-time adaptation drive progress far more effectively than scaling parameters.

### Key Findings on Reasoning Paradigms

#### Current Progress Patterns

**ARC-AGI Progress is Currently Dominated by Scaling**
- Larger models (like GPT-4, Claude, etc.) score higher
- But scaling alone hits fundamental ceilings
- Frontier models still achieve <50% on ARC-AGI-1, much lower on ARC-AGI-2

#### Human-Like Fluid Intelligence Associated with Conceptual Compression

**Core Insight:** Humans solve ARC tasks through:
1. Finding compact, high-level representations
2. Identifying underlying principles
3. Composing learned abstractions

**Current AI Limitation:** Systems struggle with abstraction and compression, instead:
- Memorizing surface patterns
- Failing to identify transferable principles
- Unable to compose learned rules in novel ways

### Taxonomy of Approaches & Detailed Classification

#### Approach Categories

1. **Neural End-to-End**
   - Transformer-based models
   - Convolutional neural networks
   - Diffusion models
   - Typical performance: 15-25% on ARC-AGI-1

2. **Symbolic Program Synthesis**
   - Program induction from examples
   - Logic programming approaches
   - Rule extraction systems
   - Typical performance: 10-30% on ARC-AGI-1

3. **Hybrid Perception-Reasoning**
   - Neural feature extraction + symbolic reasoning
   - Program synthesis with learned embeddings
   - Neural module networks
   - Typical performance: 30-45% on ARC-AGI-1

4. **Test-Time Adaptation**
   - In-context learning
   - Prompt engineering
   - Few-shot adaptation
   - Demonstrated as key to performance
   - Parameter-efficient approaches dominate

5. **Ensemble Methods**
   - Combining multiple approaches
   - Voting mechanisms
   - Complementary strengths of different methods
   - Show promise in boosting overall performance

6. **Large Language Model Approaches**
   - Direct prompting
   - Chain-of-thought reasoning
   - Constraint satisfaction formulation
   - Recent improvements with o1/o3 style models
   - Still limited by visual reasoning bottleneck

### Competition Performance & SOTA

#### Best Performing Approaches

**Top Tier (40%+ on ARC-AGI-1):**
- Hybrid systems with strong test-time refinement
- Multi-modal models with symbolic reasoning
- Systems emphasizing compositional decomposition

**Notable Recent Results:**
- GPT-5.2 and o3-style models showing significant improvements
- Parameter-efficient hybrids (TRM at 7M params achieving 45%)
- Ensemble systems combining multiple paradigms

#### Performance Ceiling Observations

**ARC-AGI-1:**
- Best systems: ~45-50%
- Average frontier models: 20-30%
- Pure neural: ~20% ceiling consistent across many approaches

**ARC-AGI-2:**
- Best systems: ~15-20%
- General frontier models: 5-10%
- Represents significant jump in difficulty

**Gap Analysis:**
- Human expert performance: 100%
- Average human: 60%
- Best AI: ~45-50% on Gen-1, ~20% on Gen-2
- Clear multi-decade gap to human-level AGI

### Detailed Technical Findings

#### What Works

1. **Compositional Reasoning**
   - Systems that decompose problems into sub-tasks perform better
   - Modularity in approach structure improves generalization
   - Hierarchy of abstractions beneficial

2. **Test-Time Adaptation**
   - In-context learning and refinement crucial
   - Iterative hypothesis refinement outperforms single-pass inference
   - Parameter-efficient adaptation more effective than scaling

3. **Hybrid Architectures**
   - Combining neural perception with symbolic reasoning most effective
   - Separation of concerns (perceive vs. reason) improves performance
   - Multiple reasoning paradigms better than single approach

4. **Constraint-Based Reasoning**
   - Formulating problems as constraint satisfaction problems effective
   - Large language models good at constraint specification
   - Symbolic solvers effective at constraint satisfaction

5. **Few-Shot Learning**
   - Critical capability for ARC tasks
   - Minimal training examples required
   - Systems must learn transformation rules from 2-5 demonstrations

#### What Doesn't Work

1. **Pure Scaling**
   - Increasing parameters without algorithmic innovation hits ceiling
   - 20% ceiling for pure neural approaches independent of scale
   - Scaling helps within approaches but doesn't overcome fundamental limitations

2. **End-to-End Learning**
   - Without compositional structure, fails to generalize
   - Memorization more likely than abstraction learning
   - Difficulty learning task-specific transformation rules

3. **Brute-Force Search**
   - Tasks specifically designed to resist brute-force approaches
   - Large search spaces make enumeration infeasible
   - Requires intelligent hypothesis generation

4. **Generic Prompting**
   - Direct prompting of LLMs without task-specific reasoning
   - Requires structured problem formulation
   - Needs integration with symbolic methods

### Field-Level Observations

#### Current State

**Phase:** Exploratory rather than converged
- No dominant superior approach yet emerged
- Multiple viable paradigms showing progress
- Significant room for innovation and improvement

**Research Directions:**
- Increasing emphasis on hybrid approaches
- Growing interest in test-time adaptation
- Focus on parameter efficiency over scaling
- Exploration of conceptual compression and abstraction

#### Research Community

- Active competition via ARC Prize (2024-2025)
- Diverse approaches from academic and industry labs
- Cross-pollination of ideas between neural and symbolic communities
- Growing emphasis on interpretability and explainability

### Implications for Competition Strategy

1. **Architecture Design**
   - Hybrid systems more likely to succeed than pure approaches
   - Compositional decomposition critical for generalization
   - Separate perception and reasoning modules

2. **Parameter Efficiency**
   - Invest in algorithmic innovation over raw scale
   - 7M-76K parameter models shown competitive
   - Test-time refinement more valuable than training-time scaling

3. **Test-Time Adaptation**
   - In-context learning essential
   - Iterative refinement and hypothesis testing
   - Multi-pass inference with feedback loops

4. **Reasoning Paradigm**
   - Formulate as constraint satisfaction or program synthesis
   - Use symbolic reasoning for rule learning
   - Neural perception for input understanding

5. **Compositional Approach**
   - Decompose into abstract sub-problems
   - Learn reusable transformation rules
   - Compose learned rules for novel tasks

6. **Learning from Minimal Data**
   - Few-shot learning critical (2-5 examples)
   - Avoid overfitting to training distribution
   - Focus on transfer to novel test tasks

---

## Cross-Paper Synthesis & Strategy Implications

### Core Capabilities Needed for ARC-AGI-2 Success

1. **Compositional Generalization** (emphasized in ARC-AGI-2)
   - Ability to combine learned rules in novel ways
   - Multi-rule and multi-step reasoning
   - Contextual rule application

2. **Symbolic Interpretation** (new emphasis in ARC-AGI-2)
   - Assign semantic meaning to visual symbols
   - Go beyond pattern matching to conceptual understanding
   - Symbol definition from context

3. **Core Knowledge Priors** (foundation)
   - Objectness and elementary physics
   - Agentness and goal-directedness
   - Natural numbers and arithmetic
   - Elementary geometry and topology

4. **Intelligence as Compression** (theoretical foundation)
   - Find compact, high-level representations
   - Learn underlying principles, not surface patterns
   - Transfer learned abstractions to novel tasks

### Recommended Solver Approach

**Architecture Type:** Hybrid neural-symbolic with test-time adaptation

**Key Components:**
1. **Perception Module:** Neural network for grid analysis and feature extraction
2. **Reasoning Module:** Symbolic reasoning for rule learning and composition
3. **Decomposition:** Break tasks into abstract sub-problems
4. **Adaptation:** In-context learning during test/evaluation phase
5. **Composition:** Combine learned rule components for novel tasks

**Efficiency Focus:**
- Parameter efficiency over scale (aim for 7M-76K parameters)
- Algorithmic innovation over brute-force search
- Iterative refinement during inference

**Evaluation:**
- Test on all three eval sets (Public, Semi-Private, Private)
- Expect calibration across sets (~<1% score difference)
- Human baseline: 60% average, 75% among task-solvers, 100% expert

---

## Source References

1. **ARC-AGI-2: A New Challenge for Frontier AI Reasoning Systems**
   - ArXiv: https://arxiv.org/html/2505.11831v2
   - Abstract: https://arxiv.org/abs/2505.11831
   - Technical Report: https://arcprize.org/blog/arc-agi-2-technical-report
   - Benchmark: https://arcprize.org/arc-agi/2

2. **On the Measure of Intelligence by François Chollet**
   - ArXiv Abstract: https://arxiv.org/abs/1911.01547
   - ArXiv HTML: https://arxiv.org/html/1911.01547v2
   - Paper Summary: https://liamwellacott.github.io/artificial%20intelligence/on-the-measure-of-intelligence/
   - Analysis: https://roberttlange.com/posts/2020/02/on-the-measure-of-intelligence/

3. **The ARC of Progress towards AGI: A Living Survey**
   - ArXiv HTML: https://arxiv.org/html/2603.13372v1
   - ARC Prize 2025 Results: https://arcprize.org/blog/arc-prize-2025-results-analysis
   - ARC Prize 2024 Technical Report: https://arcprize.org/media/arc-prize-2024-technical-report.pdf

4. **Additional References**
   - ARC Prize Guide: https://arcprize.org/guide
   - ARC Prize GitHub: https://github.com/arcprize/ARC-AGI-2
   - Epoch AI Benchmark Page: https://epoch.ai/benchmarks/arc-agi-2
   - Emergent Mind Topics: https://www.emergentmind.com/topics/arc-agi-benchmark
   - Recent Analysis: https://intuitionlabs.ai/articles/gpt-5-2-arc-agi-2-benchmark-analysis

---

## Document Metadata

- **Compiled:** March 26, 2026
- **Focus:** Competition strategy for ARC-AGI-2
- **Sources:** 3 foundational papers + supporting materials
- **Key Topics:** Benchmark structure, task categories, core priors, approach taxonomy, strategy recommendations
- **Update Frequency:** Living document (survey is updated through Dec 2025)

