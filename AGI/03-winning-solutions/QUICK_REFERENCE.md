# ARC-AGI Winning Solutions - Quick Reference
## At-a-glance comparison and key metrics

---

## 2024 Competition Winners

### 1st Place: ARChitects | 53.5% (ARC-AGI-1)
- **Tech**: Test-Time Training (TTT) + Data Augmentation
- **Model**: 8B parameter LLM with 2D attention
- **Key Innovation**: Fine-tune at test time on task demonstrations
- **Status**: ✓ Open Source

### 2nd Place (Paper): Ekin Akyürek et al | 47.5% (semi-private)
- **Tech**: TTT foundational research
- **Contribution**: Identified 3 critical TTT components
- **Key Finding**: 6× accuracy improvement vs. base model
- **Status**: ✓ Open Source (papers)

### Highest Score: MindsAI | 55.5% (ARC-AGI-1)
- **Tech**: Aggressive TTFT + Synthetic augmentation
- **Innovation**: Pioneer TTT approach (began 2023)
- **Model**: Salesforce T5 series
- **Status**: ✗ Not open sourced (ineligible for prizes)

### Alternative (Program Synthesis): Ryan Greenblatt | 50% (public leaderboard)
- **Tech**: LLM-guided program search (GPT-4o)
- **Model**: GPT-4o generating 2,048+ programs per task
- **Key Finding**: Log-linear accuracy vs. test-time compute
- **Status**: ✓ Partially open sourced

---

## 2025 Competition Winners (ARC-AGI-2 Harder)

### 1st Place: NVARC | ~24% (ARC-AGI-2)
- **Tech**: Synthetic data + TTT ensemble + TRM
- **Model**: 4B parameter fine-tuned (Qwen)
- **Cost**: $0.20 per task (most efficient)
- **Innovation**: Offline synthetic data pipeline (103K puzzles)
- **Key Components**:
  - Improved TTT component (2024 ARChitects evolution)
  - TRM component (tiny recursive model)
  - Ensemble voting
- **Status**: ✓ Open Source

### 2nd Place: ARChitects | 16.53% (ARC-AGI-2)
- **Tech**: 2D-aware masked diffusion + recursive refinement
- **Model**: LLaDA-8B with 2D RoPE positioning
- **Innovation**: Diffusion as iterative solver with soft-masking
- **Key Finding**: Perspective-based ensemble voting
- **Status**: ✓ Open Source

### 3rd Place: MindsAI | 15.42% (ARC-AGI-2)
- **Tech**: Heavily engineered TTFT + augmentation ensembles
- **Innovation**: Tokenizer dropout, new pretraining tricks
- **Approach**: Evolution of 2024 strategy with refinements
- **Status**: ✓ Partial open source

### Best Paper: TRM (Tiny Recursive Model) | 45% AGI-1 / 8% AGI-2
- **Tech**: Recursive refinement with deep supervision
- **Model**: 7M parameters (0.01% vs. frontier models)
- **Key Innovation**: Deep supervision doubled accuracy
- **Architecture**: Think→Act loop unrolled 16 times
- **Key Finding**: Parameter efficiency matters more than scale
- **Status**: ✓ Open Source

---

## Dominant Techniques Ranked

### Tier 1: Essential (55%+ potential)
1. **Test-Time Training (TTT)** - Fine-tune on task at inference time
2. **Data Augmentation** - Generate task variations (3-6× improvement)
3. **Ensemble Methods** - Combine complementary approaches
4. **Iterative Refinement** - Recursive improvement loops

### Tier 2: High Value (40-50% potential)
1. **2D Specialized Architectures** - Grid-aware position encodings
2. **Program Synthesis Guidance** - LLM-directed search
3. **Synthetic Data Generation** - Offline curriculum creation
4. **Deep Supervision** - Loss at each refinement step

### Tier 3: Supplementary (20-40% potential)
1. **Perspective-based voting** - Multiple transformations
2. **Tokenizer optimization** - Dropout, augmentation
3. **Concept decomposition** - Breaking problems into parts
4. **Learned halting** - When to stop refining

---

## Architecture Patterns

### Pattern 1: TTT-Heavy (NVARC, ARChitects 2024, MindsAI)
```
Task Input
    ↓
Fine-tune LLM on task demonstrations
    ↓
Generate predictions via token sampling
    ↓
Ensemble vote → Output
```
**Strengths**: Visual pattern matching, spatial reasoning
**Weaknesses**: Context limits, symbol semantics

### Pattern 2: Recursive Refinement (TRM, ARChitects 2025 diffusion)
```
Task Input
    ↓
[Refinement Loop: 4-16 iterations]
  - Update latent state
  - Update prediction
  - Deep supervision at each step
    ↓
Output (with learned stopping)
```
**Strengths**: Iterative improvement, small parameters
**Weaknesses**: Latency, fixed iteration budget

### Pattern 3: Program Synthesis Guided (Ryan Greenblatt)
```
Task Input
    ↓
Generate k=2,048 programs with LLM
    ↓
Validate each against examples
    ↓
Iteratively refine top candidates
    ↓
Ensemble successful programs → Output
```
**Strengths**: Interpretable, symbolic logic, logic puzzles
**Weaknesses**: Slower, requires valid syntax

### Pattern 4: Hybrid Ensemble (NVARC, top ARC-AGI-2 winners)
```
Task Input
    ├─ TTT Component
    │   └─ Fine-tuned fast model
    ├─ Recursive Component
    │   └─ TRM or recursive refinement
    └─ Optional Program Synthesis
        └─ Guided search
        ↓
Ensemble Voting → Output
```
**Strengths**: Complementary coverage, robustness
**Weaknesses**: Complexity, higher compute

---

## Performance-Cost Trade-offs

### Efficiency Leaders
| Solution | Accuracy | Cost/Task | Time/Task |
|----------|----------|-----------|-----------|
| NVARC | 24% | $0.20 | <1s |
| TRM | 8% (AGI-2) | $0.10 | 2s |
| ARChitects 2024 TTT | 53.5% (AGI-1) | $1.00 | 5s |

### Accuracy Leaders
| Solution | Accuracy | Cost/Task | Time/Task |
|----------|----------|-----------|-----------|
| MindsAI 2024 | 55.5% (AGI-1) | $5.00 | 15s |
| Ryan Greenblatt GPT-4o | 50% (AGI-1 pub) | Variable | 30s |
| ARChitects 2025 | 16.53% (AGI-2) | $1.50 | 8s |

---

## Critical Insights

### Insight 1: Refinement is Mandatory
**No static inference solution scores >11%**
- All SOTA use test-time training or recursive refinement
- Pure LLMs: 0% on ARC-AGI-2
- Inference without adaptation: fundamentally limited

### Insight 2: Ensemble Beats Single Approach
**~40% TTT + ~40% Program Synthesis ≠ 40% Ensemble**
- Actually produces 50%+ through complementary coverage
- TTT: visual/spatial tasks
- Synthesis: logic/symbolic tasks

### Insight 3: Augmentation = Force Multiplier
**3-5 examples → 30-50 effective examples**
- 6× accuracy improvement from augmentation
- Drives TTT effectiveness
- Symmetry-based and automata-based approaches work best

### Insight 4: Small Models Can Win
**4B parameters > 8B parameters > frontier models**
- NVARC won with smallest parameter model
- TRM (7M) outperforms Deepseek-R1, Gemini 2.5 Pro, o3-mini
- Efficiency + smart architecture > raw scale

### Insight 5: Deep Supervision is Key
**Deep supervision doubled TRM accuracy**
- Backpropagate through all refinement steps
- Not just final output loss
- Applies to recursive and iterative approaches

### Insight 6: ARC-AGI-1 is Solved (Mostly)
**55.5% achieved; saturation point ~70-80%**
- Dataset exposure through pretraining
- Brute force program search works for many
- ARC-AGI-2 created to prevent this
- 24% on AGI-2 shows harder domain

### Insight 7: Symbol Semantics Unsolved
**~25-30% of tasks require this**
- AI struggles with "symbol means X in context Y"
- Current approaches fail at semantic binding
- Key blocker for further progress

---

## Competition Strategy Summary

### Minimum Viable Approach (~15%)
1. Implement TTT with basic augmentation
2. Use standard LLM (fine-tune on public data)
3. 2D positional encoding modification
4. 2-model ensemble

**Effort**: 2-3 weeks, 1-2 people

### Competitive Approach (~20-25%)
1. Everything above, plus:
2. Implement program synthesis guidance
3. Careful augmentation pipeline design
4. Ensemble 3+ diverse models
5. Small synthetic data generation

**Effort**: 4-6 weeks, 2-3 people

### Championship Approach (~25%+)
1. Everything above, plus:
2. Recursive refinement with deep supervision
3. Perspective-based scoring
4. Large synthetic data curriculum
5. Architecture specialization per task type

**Effort**: 8+ weeks, 3-5 people

---

## Key Papers & Resources

### Essential Reading
- [ARC Prize 2024 Technical Report](https://arxiv.org/abs/2412.04604) - Comprehensive analysis
- [ARC Prize 2025 Technical Report](https://arxiv.org/abs/2601.10904) - ARC-AGI-2 insights
- [Less is More: Recursive Reasoning](https://arxiv.org/abs/2510.04871) - TRM breakthrough
- [The Surprising Effectiveness of Test-Time Training](https://ekinakyurek.github.io/papers/ttt.pdf) - TTT foundations

### Code Repositories
- [NVARC (Winner 2025)](https://github.com/1ytic/NVARC)
- [TinyRecursiveModels](https://github.com/SamsungSAILMontreal/TinyRecursiveModels)
- [ARChitects 2024 Kaggle](https://www.kaggle.com/code/dfranzen/arc-prize-2024-solution-by-the-architects/)

### Key Blog Posts
- [NVIDIA Technical Blog: NVARC Victory](https://developer.nvidia.com/blog/nvidia-kaggle-grandmasters-win-artificial-general-intelligence-competition/)
- [Deep Learning + Program Synthesis](https://arcprize.org/blog/beat-arc-agi-deep-learning-and-program-synthesis)

---

## Common Pitfalls to Avoid

1. **Relying on static models** → Must implement TTT
2. **Single approach** → Ensemble complementary methods
3. **Skipping augmentation** → 3-6× gain available
4. **Ignoring 2D structure** → Use 2D attention/RoPE
5. **Overfitting to AGI-1** → AGI-2 is harder, more generalizable
6. **Excess parameters** → Optimize architecture, not just scale
7. **No iterative refinement** → Refinement loops are essential
8. **Standard tokenization** → Consider specialized encodings

---

## Timeline for Development

**Week 1-2**: Baseline TTT implementation (target 15%)
**Week 3-4**: Program synthesis integration (target 20%)
**Week 5-6**: Recursive refinement + deep supervision (target 25%)
**Week 7-8**: Synthetic data pipeline (target 25-28%)
**Final week**: Hyperparameter tuning and ensemble optimization

---

*Quick reference for ARC-AGI competition strategy. See full analysis document for detailed explanations and sources.*
