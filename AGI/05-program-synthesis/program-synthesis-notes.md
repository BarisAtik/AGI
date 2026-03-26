# Program Synthesis Approaches for ARC-AGI: Research Notes

**Compilation Date:** March 26, 2026
**Research Focus:** Program synthesis methodologies, domain-specific languages (DSLs), search strategies, and validation approaches for the Abstraction and Reasoning Corpus (ARC-AGI).

---

## 1. Program Synthesis using Inductive Logic Programming for ARC

**Source:** https://arxiv.org/abs/2405.06399
**Paper Title:** Program Synthesis using Inductive Logic Programming for the Abstraction and Reasoning Corpus
**Authors:** Filipe Marinho Rocha, Inês Dutra, Vítor Santos Costa, Luís Paulo Reis
**Submission Date:** May 10, 2024

### DSL Design / Program Representation
- **Symbolic approach** using Inductive Logic Programming (ILP)
- **Manually defined simple DSL** with object-centric abstractions relevant to ARC
- **DSL Components:**
  - Objects: Point, Line, Rectangle
  - Relations: LineFromPoint, Translate, Copy, PointStraightPathTo
- Represents programs as Logic Programs capable of reasoning over spatial transformations

### Search Strategy
- **Inductive Logic Programming (ILP)** - symbolic reasoning approach
- Creates Logic Programs from few examples
- Particularly suited for ARC's input-output example pairs on grids
- Leverages symbolic AI for generalization

### Program Verification
- Validates programs against provided input-output example pairs
- Tests generalization to unseen tasks using few examples

### ARC Benchmark Results
- System capable of generalizing to unseen tasks
- Demonstrates that ILP can effectively solve ARC problems through logic program creation
- Specific metrics not detailed in search results

### Key Innovations
- **Symbolic approach alternative** to neural methods for ARC
- **Few-shot generalization** through logic program synthesis
- Integration of object-centric abstractions matching ARC's spatial reasoning demands
- Overcomes neural network limitations (noted weakness of LLMs on ARC)

### Scalability Considerations
- Manual DSL design limits adaptability to new domains
- ILP computational complexity scales with search space
- Reliant on well-designed background knowledge
- More interpretable than neural approaches but potentially less flexible

---

## 2. Structured Program Synthesis using LLMs: IPARC Challenge

**Source:** https://arxiv.org/abs/2506.13820
**Paper Title:** Structured Program Synthesis using LLMs: Results and Insights from the IPARC Challenge
**Authors:** Shraddha Surana, Ashwin Srinivasan, Michael Bain
**Submission Date:** June 15, 2025

### DSL Design / Program Representation
- **IPARC Challenge benchmark:** 600 controlled program synthesis tasks over synthetic images
- Focuses on three fundamental control structures:
  - Sequence
  - Selection (conditionals)
  - Iteration (loops)
- Tasks designed to test automated program construction in a controlled setting

### Search Strategy
- **Structured inductive programming approach with LLMs**
- Combines program structure discovery with LLM-based code generation
- Emphasis on prior structuring before LLM application
- Requires human refinement of LLM-generated structure

### Program Verification
- Validation against synthetic image transformations
- Code correctness verification through execution on test cases
- Integration of correctness checking into the synthesis loop

### ARC Benchmark Results
- Successfully solves tasks across all IPARC categories (A: easy, B: hard, C: varied difficulty)
- Demonstrates viability of structured approaches on previously intractable synthesis problems
- Shows promise for human-LLM collaborative synthesis

### Key Innovations
- **Structured synthesis pipeline:** Breaking complex tasks into discoverable structure patterns
- **Human-in-the-loop approach:** LLMs generate candidates, humans refine structure
- **Code freezing:** Once correct code is identified, prevent regression in subsequent iterations
- **Code reuse efficiency:** Demonstrates value of reusing verified code components
- **Cross-category generalization:** Insights applicable across different problem structures

### Scalability Considerations
- Requires human intervention for structure refinement
- Manual code freezing needed for stability
- Structured approach less flexible for novel domains
- But significantly reduces LLM search space through structural constraints
- Demonstrates human-LLM collaboration can outperform pure automation

---

## 3. Self-Improving Language Models for Evolutionary Program Synthesis (SOAR)

**Source:** https://arxiv.org/abs/2507.14172
**Paper Title:** Self-Improving Language Models for Evolutionary Program Synthesis: A Case Study on ARC-AGI
**Authors:** Julien Pourcel, Cédric Colas, Pierre-Yves Oudeyer
**Publication Venue:** Proceedings of the 42nd International Conference on Machine Learning (ICML), 2025

### DSL Design / Program Representation
- **No hand-engineered DSL required**
- Open-source LLM generates programs directly in Python/general programming language
- Leverages learned program distributions from fine-tuning

### Search Strategy
- **Evolutionary program synthesis with self-improvement loop:**
  1. **Evolutionary Search Phase:** LLM samples and refines candidate solutions
  2. **Hindsight Learning Phase:** Converts search attempts into valid problem-solution pairs
  3. **Fine-tuning:** Model improves its sampling and refinement capabilities
  4. Cycle repeats with enhanced LLM
- Each iteration increases search effectiveness by improving underlying model

### Program Verification
- Execution-based validation against input-output examples
- Programs must produce correct outputs on all provided examples
- Hindsight learning extracts successful patterns from failed attempts

### ARC Benchmark Results
- **Public test set performance: 52%** (ensemble across multiple model sizes and iterations)
- Overcomes typical performance plateaus when scaling model size or search budget
- Smaller models sometimes solve tasks larger models miss
- Multi-model ensembling yields strongest improvements
- Training on aggregated solutions from multiple iterations critical to performance

### Key Innovations
- **Self-improving loop:** Model improves itself through its own search experience
- **Hindsight extraction:** Converting failed attempts into learning signals
- **Scaling escape:** Moving beyond conventional scaling laws by improving the model itself
- **No DSL dependency:** Demonstrates pure LLM-based approach can be competitive
- **Test-time adaptation:** Improvements during training carry over to inference
- **Ensemble effectiveness:** Combining models across sizes and iterations

### Scalability Considerations
- Iterative fine-tuning requires significant computational resources
- Hindsight extraction scales with number of search attempts
- Multiple fine-tuning iterations needed for performance gains
- Ensemble at test time increases inference cost
- However, eliminates need for manual DSL engineering
- Potentially more generalizable across different task domains

---

## 4. ConceptSearch: Efficient Program Search Using LLMs

**Source:** https://arxiv.org/abs/2412.07322
**Paper Title:** ConceptSearch: Towards Efficient Program Search Using LLMs for Abstraction and Reasoning Corpus (ARC)
**Authors:** Kartik Singhal, Gautam Shroff
**Submission Date:** December 10, 2024
**Code:** https://github.com/kksinghal/concept-search

### DSL Design / Program Representation
- LLM-based program generation (uses GPT-4 in experiments)
- Programs evaluated on semantic understanding of transformation concepts
- Implicit DSL learned from LLM training

### Search Strategy
- **Concept-based scoring function** guides search efficiently
- Evaluates programs on ability to capture underlying transformation concept
- Not reliant on pixel-level metrics
- Leverages semantic understanding of what the transformation represents

### Program Verification
- **Concept-based evaluation:** Does the program capture the transformation rule?
- Distinction from simple pixel-matching: evaluates correctness of learned concept
- Verification through semantic alignment with examples

### ARC Benchmark Results
- **30% greater efficiency** than Hamming distance baseline
- Measured by iterations required to reach correct solution
- Significant performance improvement over direct GPT-4 prompting

### Key Innovations
- **Concept-based scoring:** Moving beyond Hamming distance metrics
- **Semantic guidance:** Programs evaluated on conceptual correctness rather than output matching
- **Efficiency gain:** 30% fewer iterations needed compared to standard metrics
- **LLM-native approach:** Leverages LLM's semantic understanding directly

### Scalability Considerations
- Search efficiency improves with better concept detection
- Concept quality depends on underlying LLM capabilities
- Potentially more transferable across domains than pixel-based approaches
- Computational cost depends on LLM query frequency and concept evaluation

---

## 5. Execution Guided Line-by-Line Code Generation

**Source:** https://arxiv.org/abs/2506.10948
**Paper Title:** Execution Guided Line-by-Line Code Generation
**Authors:** Boaz Lavon, Shahar Katz, Lior Wolf
**Submission Date:** June 12, 2025
**Revised:** October 23, 2025

### DSL Design / Program Representation
- No explicit DSL - direct program generation in standard programming languages
- Programs generated line-by-line with execution feedback
- Maintains syntactic coherence across line boundaries

### Search Strategy
- **Execution-Guided Classifier-Free Guidance (EG-CFG)** during generation
- Incorporates real-time execution signals as model generates code
- Provides line-by-line feedback during inference (not just post-hoc validation)
- Maintains consistent guidance signals within lines, refreshes at line boundaries

### Program Verification
- **Real-time execution feedback** during generation process
- Programs validated at line boundaries
- Execution signals guide model toward syntactically and functionally valid solutions

### ARC Benchmark Results
- State-of-the-art results across diverse coding tasks
- Performance improvements demonstrated across:
  - Foundational problems
  - Challenging competitive programming
  - Data science tasks

### Key Innovations
- **Execution signals during inference:** Unlike typical LLM generation that ignores execution
- **Line-by-line guidance:** Coherent feedback at program structure level
- **Classifier-free guidance integration:** Incorporating execution as guidance signal
- **Dynamic token guidance:** Leverages execution information as generation progresses

### Scalability Considerations
- Requires execution environment available during inference
- Execution overhead during generation (line-by-line validation)
- More computational cost than standard generation
- But significantly improves code quality and reduces invalid outputs
- Potentially reduces need for extensive search/verification phases

---

## 6. DreamCoder: Foundational Work in Library Learning

**Source:** Multiple (PLDI 2021)
**Paper Title:** DreamCoder: Bootstrapping Inductive Program Synthesis with Wake-Sleep Library Learning
**Authors:** Kevin Ellis et al.
**Publication Venue:** 42nd ACM SIGPLAN International Conference on Programming Language Design and Implementation (PLDI 2021)
**Key References:**
- [ACM Digital Library](https://dl.acm.org/doi/10.1145/3453483.3454080)
- [MIT Handle](https://dspace.mit.edu/handle/1721.1/145949)
- [NSF Public Access](https://par.nsf.gov/biblio/10320121-dreamcoder-bootstrapping-inductive-program-synthesis-wake-sleep-library-learning)

### DSL Design / Program Representation
- **Dynamic DSL construction** through library learning
- Starts with basic primitives and abstractions
- Expands library with discovered higher-level abstractions
- E-graph based refactoring for common subcomponent identification

### Search Strategy
- **Wake-sleep algorithm variant:**
  - **Wake phase:** Generate programs using neural network search policy
  - **Sleep phase:** Grow the DSL library with discovered abstractions
  - Iterate to bootstrap better library and search policy together
- Neural search policy guides exploration within current DSL

### Program Verification
- Programs validated against provided examples for each problem domain
- Wake phase synthesizes programs, sleep phase validates and abstracts

### ARC Benchmark Results / General Performance
Demonstrated on 8 domains including:
- Program synthesis benchmarks
- Planning
- Inverse graphics
- Equation discovery

**Text editing domain example:**
- Before learning: 3.7% success rate on 10-minute timeout
- After learning: 79.6% success rate
- Average solving time: 40 seconds per problem

### Key Innovations
- **Library bootstrapping:** Self-improving DSL construction
- **Wake-sleep mutual improvement:** Library and search policy bootstrap each other
- **Interpretable abstractions:** Discovered libraries are human-readable
- **Hierarchical knowledge:** Captures domain structure through abstraction hierarchy
- **Generalizable approach:** Framework applicable across domains

### Scalability Considerations
- Library learning improves with more problems (domain expansion)
- Sleep phase computational cost scales with program complexity
- Discovered abstractions reduce subsequent search space dramatically
- Approach shows strong improvement curves with more training examples
- Computationally intensive but produces interpretable, reusable knowledge

---

## Comparative Analysis: Search Strategies

### Symbolic Approaches (ILP)
- **Pros:** Interpretable, strong theoretical grounding, few-shot learning
- **Cons:** Manual DSL design required, limited domain adaptability
- **Best for:** Well-structured domains with clear abstractions (e.g., spatial reasoning)

### Evolutionary + Self-Improvement (SOAR)
- **Pros:** No manual DSL, self-improving, strong empirical results (52%), ensemble effective
- **Cons:** Computationally expensive, requires iterative fine-tuning
- **Best for:** Open-ended tasks, domains where DSL is hard to define

### LLM + Structured Guidance (IPARC, ConceptSearch)
- **Pros:** Human-interpretable structure, concept-based evaluation, efficient search
- **Cons:** Requires human involvement (IPARC), LLM-dependent quality (ConceptSearch)
- **Best for:** Structured domains, human-in-the-loop scenarios

### Execution-Guided Generation (EG-CFG)
- **Pros:** Real-time feedback, syntactic coherence, state-of-the-art code quality
- **Cons:** Inference overhead, requires execution environment
- **Best for:** Code generation tasks where execution feedback available

### Library Learning (DreamCoder)
- **Pros:** Builds interpretable DSL, mutual improvement, highly efficient once learned
- **Cons:** Significant up-front computational cost, needs sufficient domain examples
- **Best for:** Domains with recurring patterns, interpretability important

---

## ARC-AGI Specific Insights

### Performance Trajectory (2020-2025)
- 2020: Winner achieved 19% with brute-force program search
- Recent: Refined approaches reach 36% (brute-force with optimizations)
- 2025 SOTA: 52% with SOAR (ensemble approach)

### Emerging Trend: The Refinement Loop
- Per-task iterative optimization guided by feedback signal
- Self-improving approaches gaining dominance
- Evolutionary program synthesis with LLMs showing strongest results

### DSL vs. No-DSL Tradeoff
- **DSL-based:** Reduced search space, but manual engineering overhead
- **Open-ended LLMs:** No engineering cost, but larger search space
- **Hybrid:** Best results combining structured guidance with neural search

### Critical Success Factors
1. **Effective scoring/feedback:** Concept-based (not pixel-based) metrics
2. **Iterative self-improvement:** Models learning from their own search
3. **Ensemble methods:** Multiple models/sizes solve complementary problems
4. **Human-machine collaboration:** Structured guidance from humans, generation from LLMs
5. **Code reuse:** Freezing correct components, building on successes

---

## Research Gaps and Open Questions

1. **DSL Expressiveness:** How minimal can a DSL be while maintaining expressiveness?
2. **Sample Efficiency:** Can self-improving approaches match symbolic sample efficiency?
3. **Generalization:** Do learned programs/abstractions transfer across domains?
4. **Scalability:** What is computational ceiling for iterative self-improvement?
5. **Interpretability:** Can self-improving LLM approaches maintain interpretability?
6. **Human-AI Collaboration:** What is optimal division of labor in structured synthesis?

---

## Recommended Further Investigation

1. **SOAR Implementation Details:** Fine-tuning procedures, convergence criteria
2. **ConceptSearch Metrics:** How are concepts extracted and evaluated?
3. **DreamCoder E-graphs:** Specific refactoring algorithms and abstraction discovery
4. **Ensemble Strategies:** Optimal combination of model sizes and iterations
5. **Domain Transfer:** How well do approaches transfer between task domains?

---

## References

1. [Program Synthesis using Inductive Logic Programming for ARC (2405.06399)](https://arxiv.org/abs/2405.06399)
2. [Structured Program Synthesis using LLMs: IPARC Challenge (2506.13820)](https://arxiv.org/abs/2506.13820)
3. [Self-Improving Language Models for Evolutionary Program Synthesis: SOAR (2507.14172)](https://arxiv.org/abs/2507.14172)
4. [ConceptSearch: Efficient Program Search Using LLMs (2412.07322)](https://arxiv.org/abs/2412.07322)
5. [Execution Guided Line-by-Line Code Generation (2506.10948)](https://arxiv.org/abs/2506.10948)
6. [DreamCoder: Bootstrapping Inductive Program Synthesis with Wake-Sleep Library Learning (PLDI 2021)](https://dl.acm.org/doi/10.1145/3453483.3454080)
7. [ARC Prize 2025 Results and Analysis](https://arcprize.org/blog/arc-prize-2025-results-analysis)
8. [How to Beat ARC-AGI by Combining Deep Learning and Program Synthesis](https://arcprize.org/blog/beat-arc-agi-deep-learning-and-program-synthesis)

---

**Document Status:** Completed research compilation
**Last Updated:** March 26, 2026
