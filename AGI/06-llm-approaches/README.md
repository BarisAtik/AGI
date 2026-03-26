# LLM and Neuro-Symbolic Approaches for ARC-AGI Research

## Contents

### Main Document
- **llm-and-neurosymbolic-notes.md** (956 lines, 36KB)
  - Comprehensive synthesis of 11 major research sources
  - Detailed technical analysis of architecture, methods, results, strengths/weaknesses, and computational requirements
  - Comparative performance tables and architectural analysis
  - Future research directions

## Document Structure

1. **SECTION 1: LLM-BASED APPROACHES** (6 approaches)
   - Reasoning Abilities Analysis (2403.11793)
   - Object-Based Representations (2305.18354)
   - Product of Experts (2505.07859) - 71.6% SOTA
   - GPT-4o by Redwood (50% breakthrough)
   - Deep Learning TTT (2506.14276)
   - Hierarchical Reasoning Model (2506.21734) - 40.3% with 27M parameters

2. **SECTION 2: NEURO-SYMBOLIC APPROACHES** (4 approaches)
   - Object-Centric Models with MDL (2311.00545)
   - MIT Thesis on Neurosymbolic Methods (2021)
   - Imbue's Code Evolution (95.1% on Gemini 3.1 Pro)
   - ARC-AGI-2 Technical Report (Hybrid neural-symbolic)

3. **SECTION 3: COMPARATIVE ANALYSIS**
   - Performance summary table
   - Architectural comparison
   - Key technical insights
   - Trade-off analysis

4. **SECTION 4: SYNTHESIS**
   - Current limitations
   - Future research directions
   - Theoretical gaps

5. **SECTION 5: COMPLETE SOURCE REFERENCES**
   - All 11+ sources with URLs
   - GitHub repositories
   - Blog posts and technical reports

## Key Findings

### Performance Rankings (as of March 2026)
1. Imbue Evolution (Gemini 3.1 Pro): **95.1%** ($8.71/task)
2. Product of Experts (GPT-4): **71.6%** ($0.02/task)
3. Redwood GPT-4o: **50.0%** (~$1-10/task)
4. Hierarchical Model: **40.3%** (~$0.01/task, 27M params)

### Architectural Patterns
- **Best Performance:** Evolutionary + LLM (Imbue)
- **Best Efficiency:** Hierarchical Model (27M parameters)
- **Best Value:** Product of Experts (71.6% at $0.02)
- **Most Interpretable:** Object-Centric + MDL

## Research Highlights

### LLM-Based Findings
- Object-centric representations nearly **double LLM performance**
- Composition tasks remain weak (3-14% accuracy on DSL)
- Test-time adaptation enables rapid per-task learning
- Ensemble methods provide significant gains

### Neuro-Symbolic Findings
- MDL principle effectively guides model selection
- Symbolic priors eliminate invalid solutions
- Symmetry constraints improve generalization
- Bidirectional reasoning complements forward synthesis

### Hybrid Findings
- Evolutionary optimization adds **7-27%** to base LLM performance
- Cost-effectiveness improves with evolution on weaker models
- Multi-perspective reasoning through symmetry augmentation works well

## Quick Reference

### All Approaches at a Glance

| Approach | Type | Performance | Cost | Efficiency |
|----------|------|-------------|------|-----------|
| Product of Experts | LLM Ensemble | 71.6% | $0.02 | Medium |
| Imbue Evolution | Hybrid | 95.1% | $8.71 | Low |
| Hierarchical Model | Deep Learning | 40.3% | <$0.01 | High |
| Redwood GPT-4o | LLM-based | 50.0% | $1-10 | Low |
| Object-Centric MDL | Neuro-Symbolic | Unknown | Unknown | High |
| MIT Bidirectional | Neuro-Symbolic | Unknown | Unknown | Medium |
| ARC-AGI-2 System | Hybrid | Not specified | Medium | Medium |

## Research Methodology

All information extracted from:
- arXiv papers (peer-reviewed preprints)
- Official blog posts (Redwood, ARC Prize, Imbue)
- MIT thesis (academic research)
- GitHub repositories (open-source implementations)
- Technical reports (ARC Prize official)

## Usage

For researchers implementing these approaches:
1. Start with Product of Experts for quick baselines (71.6%, low cost)
2. Study Hierarchical Model for efficiency insights (27M params, 40.3%)
3. Explore Imbue's evolution framework for performance improvements
4. Reference MIT thesis for neuro-symbolic foundations
5. Examine ARC-AGI-2 report for hybrid design principles

## Future Work

Areas identified as needing further research:
- Reducing computational costs of high-performance methods
- Understanding why different approaches work
- Generalizing beyond ARC to broader reasoning tasks
- Improving compositional reasoning in LLMs
- Scaling neuro-symbolic approaches
- Creating unified frameworks combining neural and symbolic methods

---

**Compiled:** March 26, 2026
**Data as of:** March 2026 (latest ARC-AGI-2 results included)
**Total Sources:** 11+ peer-reviewed and technical sources
