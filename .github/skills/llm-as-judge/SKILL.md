---
name: llm-as-judge
description: Built-in LLM-as-Judge evaluation for Copilot/Claude. Score LLM responses, compare models, detect hallucinations, and verify quality—all within the agent context. No external APIs. Supports single-agent and multi-agent (sequential consensus) evaluation with improved sub-agent prompts for deeper reasoning. Use when comparing responses, validating output quality, checking for hallucinations, or performing model comparisons.
version: 1.3.0
allowed-tools: Read, Write
---

# LLM-as-Judge Skill

Built-in evaluation capability for Claude/Copilot agents. Evaluate and compare LLM responses directly within the agent's reasoning process without external API calls.

## How It Works

The agent uses its own reasoning to evaluate responses without external calls:

1. **You provide** — Two or more responses to compare, or criteria to score against
2. **Agent evaluates** — Internal reasoning, no API calls
3. **Agent returns** — Structured judgment (score, verdict, reasoning)
4. **Results stored** — JSON or markdown for reference

**No external dependencies. No scripts. No API calls.** The agent handles the entire evaluation within its context.

## When to Use This Skill

- **Compare LLM outputs** — "Which response is better?" Agent uses internal reasoning
- **Score response quality** — "Rate this 1-10 on relevance/accuracy/clarity" — Agent evaluates directly
- **Detect hallucinations** — "Check if this response hallucinated facts" — Agent reasoning-based detection
- **Verify grounding** — "Is this RAG response grounded in the context?" — Agent-native evaluation
- **Code quality assessment** — "Evaluate this generated code" — Agent code review
- **Model comparison** — "Compare responses from two models" — Agent arbitration

## Core Concepts

### Judge Model

The agent itself acts as the judge. It evaluates responses using its internal knowledge and reasoning without making external API calls.

**Key characteristics:**
- Built-in to the agent (Copilot/Claude)
- Uses reasoning within the model's context
- No API keys or external services
- Transparent reasoning (you see the evaluation logic)
- Immediate results (no latency)

### Evaluation Approaches

Evaluation techniques the agent can apply:

#### 1. Rubric-Based Evaluation (Recommended)
Generates evaluation questions (rubrics) then scores against them. Most reliable.

**Pattern:**
```
Step 1: Agent generates rubrics (yes/no questions) based on the task
- "Is the response factually accurate?"
- "Does it address all requirements?"
- "Is the tone appropriate?"

Step 2: Agent evaluates response against each rubric
- Answer each question: yes/no/partial

Step 3: Agent aggregates scores
- Overall score: 0-1 (or 1-5)
- Per-rubric results for transparency
```

**Use when:** You want detailed, explainable evaluation scores.

#### 2. Direct Comparison (Pairwise)
Agent compares two responses head-to-head on defined criteria.

**Pattern:**
```
Criterion 1 (Accuracy): Response A [score] vs Response B [score] → Winner: A
Criterion 2 (Clarity): Response A [score] vs Response B [score] → Winner: B
Criterion 3 (Completeness): Response A [score] vs Response B [score] → Winner: A
Overall: Response A wins 2/3 criteria
```

**Use when:** You need to pick the better of two outputs.

#### 3. Hallucination Detection (Semantic Validity)
Agent checks if claims are supported by provided context/knowledge.

**Pattern:**
```
Context: "Python released in 1991"
Response: "Python was released in 1990. Latest version is 4.0."

Claim 1: "Python released in 1990" → UNSUPPORTED (contradicts context)
Claim 2: "Latest version is 4.0" → UNSUPPORTED (no evidence provided)
Hallucination Score: 100% (2/2 claims unsupported)
```

**Use when:** You're checking RAG responses or fact-based content.

#### 4. Instruction Compliance
Agent checks if response follows specific requirements.

**Pattern:**
```
Requirements:
   1. Under 300 words? YES
   2. Uses examples? YES
   3. Explains reasoning? PARTIAL
   4. Professional tone? YES
   
Compliance Score: 3.5/4 = 88%
```

**Use when:** Evaluating task-specific requirements (length, format, style).

#### 5. Multi-Dimensional Scoring
Agent rates on multiple quality dimensions simultaneously.

**Pattern:**
```
Accuracy: 8/10 (mostly correct, minor detail missed)
Relevance: 9/10 (directly addresses question)
Clarity: 7/10 (dense in places)
Completeness: 8/10 (covers main points)
Tone: 9/10 (professional and empathetic)

AVERAGE: 8.2/10
```

**Use when:** You need comprehensive quality assessment.

#### 6. Structured Scoring
Agent produces machine-readable scores (JSON) for aggregation.

**Pattern:**
```json
{
  "overall_score": 0.82,
  "dimensions": {
    "accuracy": 0.85,
    "relevance": 0.90,
    "clarity": 0.70,
    "completeness": 0.80,
    "tone": 0.90
  },
  "verdict": "GOOD",
  "rationale": "..."
}
```

**Use when:** You're collecting results for reporting/analysis.
- **Context Comparison** — Agent checks if claims are grounded in provided facts
- **Pattern Recognition** — Agent identifies common issues (hallucinations, logical errors, etc.)
- **Rubric-Based** — Agent applies detailed evaluation criteria you provide

### Evaluation Dimensions

Common scoring criteria the agent uses:

- **Relevance** — Does the response address the query?
- **Accuracy** — Is the information factually correct?
- **Completeness** — Does it cover all aspects of the question?
- **Clarity** — Is the response understandable and well-structured?
- **Coherence** — Is there logical flow and consistency?
- **Hallucination** — Does it invent facts not supported by context?
- **Toxicity** — Does it contain harmful content?
- **Alignment** — Does it follow instructions and safety guidelines?

## Multi-Agent Evaluation

For critical evaluation decisions, you can invoke **multiple agents sequentially** (one at a time) with different models to build consensus and improve reliability.

### How Sequential Multi-Agent Works

```
Your Evaluation Request
        ↓
Agent 1 (Claude Sonnet latest) evaluates → Result 1
        ↓
Agent 2 (GPT-5.4 or latest) evaluates → Result 2
        ↓
Agent 3 (Gemini Pro latest) evaluates → Result 3
        ↓
Aggregate & Compare Results
        ↓
Consensus Verdict: "2/3 agents agree" or "Mixed signals"
```

**Why use multiple agents?**

| Scenario | Benefit |
|----------|---------|
| **High Stakes** | Different models catch different issues (hallucinations, tone, clarity) |
| **Complex Evaluation** | Different model families (Claude, OpenAI, Google) catch different blind spots |
| **Debate/Arbitration** | When agents disagree, disagreement itself is informative |
| **Reliability** | Consensus (2/3 or 3/3 agree) = higher confidence in verdict |
| **Model Comparison** | Understand how different models evaluate (strengths/weaknesses) |

### Sequential Invocation (Not Parallel)

Copilot doesn't efficiently run agents in parallel. Use **sequential** invocation:

```
❌ DON'T try parallel agents - Copilot will serialize anyway (slower, messier)

✓ DO invoke sequentially:
   1. Call Agent 1 via @agent-1 or conversation
   2. Wait for Agent 1 result
   3. Call Agent 2 with same inputs
   4. Wait for Agent 2 result
   5. Compare & aggregate
```

### Result Aggregation

After all agents evaluate, aggregate results:

```
Agent 1 (Claude Sonnet):  Score: 8.5/10, Verdict: GOOD
Agent 2 (GPT-5.4):        Score: 8/10,   Verdict: GOOD
Agent 3 (Gemini Pro):     Score: 7.5/10, Verdict: ACCEPTABLE

Consensus Score: (8.5 + 8 + 7.5) / 3 = 8.0/10
Consensus Verdict: GOOD (3/3 agree direction)
Confidence: HIGH (low variance)
Best insight: Claude Sonnet noted missing error handling (relevant)
```

---

## Implementation Patterns

### Pattern -1 — Sequential Multi-Agent Evaluation (Consensus-Based)

**Use case:** High-stakes evaluation requiring multiple perspectives and consensus

**Setup:** Multiple agents available (Claude Sonnet, GPT-5.4, Gemini Pro, or alternates)

```
You: "Evaluate this code using multiple agents. I need consensus.

Code to evaluate:
{code}

Requirements:
- Check for: correctness, performance, maintainability, safety
- Rate each: 1-5
- Verdict: PASS/FAIL

Use 3 different evaluation agents sequentially:
1. Claude Opus (strongest reasoning)
2. Claude Sonnet (balanced) 
3. Claude Haiku (fast verification)

For each agent:
  a) Provide the same evaluation criteria
  b) Ask to evaluate independently
  c) Capture the verdict and reasoning
  
Then aggregate results showing:
- Each agent's verdict
- Agreement/disagreement patterns
- Consensus verdict
- Confidence level"

---

Agent 1 (Claude Sonnet latest) evaluates:
[Agent 1 reasoning and scoring...]
Verdict: PASS (8/10) - "Code is correct and performant"

Agent 2 (GPT-5.4 or latest) evaluates:
[Agent 2 reasoning and scoring...]
Verdict: PASS (7/10) - "Correct but could optimize memory usage"

Agent 3 (Gemini Pro latest) evaluates:
[Agent 3 reasoning and scoring...]
Verdict: PASS (7/10) - "Works correctly, needs refactoring for clarity"

---

CONSENSUS RESULTS:
Score (average): 7.3/10
Verdict agreement: 3/3 PASS
Confidence: HIGH

Agent Agreement:
- Claude Sonnet: 8/10 PASS
- GPT-5.4: 7/10 PASS
- Gemini Pro: 7/10 PASS

Agreement Matrix:
- Correctness: All 3 agree [OK]
- Performance: 2/3 concerned
- Maintainability: 2/3 raised concerns
- Safety: All 3 agree [OK]

Recommendation: ACCEPT with improvements
Priority fixes: Performance optimization, code clarity
```

**When to use:**
- Critical code reviews
- High-stakes decisions (compliance, security)
- When you need to know "do most models agree?"
- To understand model-specific blind spots

**Workflow:**
1. Write your evaluation criteria once
2. Invoke Agent 1, capture results
3. Invoke Agent 2 with same criteria
4. Invoke Agent 3 with same criteria
5. Aggregate and compare verdicts
6. Note where agents diverge (often most interesting!)

---

### Pattern 0 — Rubric-Based Evaluation (Most Reliable)

**Use case:** Comprehensive evaluation with justified scores

Based on: [generative-ai/gemini/evaluation](generative-ai/gemini/evaluation/evaltask_approach/rubric_based_eval.ipynb)

```
Step 1. You provide response + evaluation task:

You: "Generate rubrics then evaluate this response:

Task: '{task}'

Response: '{response}'

Generate yes/no questions to evaluate it, then score the response against each rubric."

Step 2. Agent generates rubrics:

Agent:
Rubric 1: "Is the response factually accurate?"
Rubric 2: "Does it address all requirements?"
Rubric 3: "Is the explanation clear?"
Rubric 4: "Is the tone appropriate?"

Step 3. Agent evaluates response against each rubric:

Rubric 1: YES - All facts verified against context
Rubric 2: YES - All 4 requirements addressed
Rubric 3: MOSTLY - Clear but one section is dense
Rubric 4: YES - Professional and friendly

Per-rubric results:
- Rubric 1: ✓
- Rubric 2: ✓
- Rubric 3: ~
- Rubric 4: ✓

Overall score: 3.75/4 = 94%
```

**Why this pattern:** Explicit rubrics = explainable scoring = easier to audit and improve.

---

### Pattern 1 — Direct Comparison

**Use case:** Quickly determine which response is better

```
You: "Compare these two responses. Which is better?

Response A: {response_a}

Response B: {response_b}

Query/Context: {context}"

Agent:
Winner: [A/B/TIE]
Reason: [Agent reasoning]
Strengths of winner: [list]
Areas for improvement: [list]
```

**No setup needed.** The agent evaluates directly using internal reasoning.

---

### Pattern 2 — Structured Quality Scoring

**Use case:** Rate response on multiple dimensions

```
You: "Score this response 1-5 on each dimension:

Response: {response}

Dimensions:
1. Accuracy (technical correctness)
2. Clarity (understandability)
3. Completeness (covers all aspects)
4. Examples (includes concrete samples)
5. Tone (appropriate for audience)"

Agent:
- Accuracy: 4/5 — Mostly correct, one edge case missed
- Clarity: 5/5 — Very clear and well-explained
- Completeness: 3/5 — Misses error handling
- Examples: 4/5 — Good examples, could use more
- Tone: 5/5 — Professional and engaging

Average: 4.2/5
```

---

### Pattern 3 — Hallucination Detection

**Use case:** Verify if claims are grounded in provided context

```
You: "Check this response for hallucinations.

Context: {context}

Response to evaluate: {response}

Instructions:
- Identify claims NOT in the context
- Identify claims that CONTRADICT the context
- Mark claims that ARE grounded
- Provide a verdict: PASS / PARTIAL / FAIL"

Agent:
Unsupported claims:
1. [claim] - not mentioned in context
2. [claim] - contradicts context

Grounded claims:
1. [claim] - directly from context
2. [claim] - supported by context

Verdict: PARTIAL HALLUCINATION (2 unsupported claims)
```

---

### Pattern 4 — Head-to-Head Model Comparison

**Use case:** Compare how different models handled the same task

```
You: "Compare these responses from different models.

Task: {task}

Model A Response: {response_a}

Model B Response: {response_b}

Evaluate on: Accuracy, Clarity, Completeness, Creativity, Safety"

Agent:
Model A:
- Accuracy: 4/5
- Clarity: 4/5
- Completeness: 5/5
- Creativity: 3/5
- Safety: 5/5
Average: 4.2/5

Model B:
- Accuracy: 5/5
- Clarity: 5/5
- Completeness: 4/5
- Creativity: 5/5
- Safety: 4/5
Average: 4.6/5

Winner: Model B (edge in creativity and accuracy)
```

---

### Pattern 5 — Code Quality Review

**Use case:** Evaluate generated code

```
You: "Review this generated code:

Code: {code}

Task: {task}

Check for:
- Correctness (solves the problem)
- Readability (code style)
- Efficiency (performance)
- Safety (error handling)
- Best practices (language conventions)"

Agent:
Correctness: ✓ Correctly solves the problem
Readability: ✓ Clear variable names, good structure
Efficiency: ~ Could use caching for repeated calls
Safety: Issue: Missing null check on line 5
Best practices: ✓ Follows PEP 8 conventions

Summary: Good code, needs error handling fix
```

---

### Pattern 6 — RAG Response Grounding

**Use case:** Verify retrieval-augmented generation quality

```
You: "Evaluate this RAG response:

Query: {query}

Retrieved Context: {context}

Generated Response: {response}

Check:
1. Is the response grounded in the context?
2. Does it accurately use the retrieved information?
3. Does it add unsupported information?"

Agent:
Grounding score: 4/5 (mostly grounded with one assumption)

Grounded claims:
- [claim] from {section}
- [claim] from {section}

Assumptions/Additions:
- [assumption] - reasonable but not in context
- [addition] - factual but not from retrieval

Verdict: GOOD (well-grounded with minor inference)
```

---

## Best Practices

- **Be specific** — Provide full context and clear evaluation criteria
- **Use rubrics** — Define what each score means (e.g., 5="excellent", 3="acceptable")
- **Include examples** — Show good and bad evaluations so agent calibrates correctly
- **Ask for reasoning** — Request explanations for scores, not just numbers
- **Verify consistency** — Check agent evaluation on multiple similar responses
- **Provide context** — The more background, the better the evaluation
- **Chain of thought** — Ask agent to "think through step by step"

## Common Pitfalls

### Pitfall: Vague Criteria
**Problem:** "Is this good?" — Agent doesn't know what "good" means
**Solution:** Be specific: "Is this accurate, clear, and complete? Rate 1-5 on each."

### Pitfall: Insufficient Context
**Problem:** Agent can't verify hallucinations without knowing what facts are true
**Solution:** Always provide source material or accepted facts to evaluate against

### Pitfall: Contradictory Instructions
**Problem:** "Rate this 1-10 but also tell me if it's perfect"
**Solution:** Use consistent scales and clear definitions

### Pitfall: Ambiguous Scoring
**Problem:** What does a "3" mean vs a "4"? Agent may be inconsistent
**Solution:** Define your scale: 5=excellent, 4=good, 3=acceptable, 2=flawed, 1=broken

## Resources

- **Judge Prompt Templates** — See `references/judge-templates.md` for reusable templates
- **Practical Use Cases** — See `references/use-cases.md` for real-world examples
- **Evaluation Approaches** — See `references/evaluation-approaches.md` for patterns and strategies

## References & Sources

This skill incorporates evaluation patterns and best practices from:

### Rubric-Based Evaluation
- **Source:** `generative-ai/gemini/evaluation/evaltask_approach/rubric_based_eval.ipynb`
- **Pattern:** Generate evaluation rubrics (yes/no questions), then score responses against them
- **Why:** Explainable, reproducible, and easier to audit evaluation results

### Reward Scoring & Automatic Evaluation
- **Source:** `ai-engineering-hub/art_mcp_rl/` (RULER - LLM-as-judge for automatic reward scoring)
- **Pattern:** Automatic evaluation without hand-labeled data
- **Application:** Multi-dimensional scoring for reinforcement learning feedback

### Model Comparison Frameworks
- **Source:** `generative-ai/gemini/evaluation/evaltask_approach/compare_generative_ai_models.ipynb`
- **Pattern:** Head-to-head comparison across defined metrics
- **Metrics:** Accuracy, Clarity, Completeness, Relevance, Tone, Safety

### RAG Evaluation Quality
- **Source:** `ai-engineering-hub/eval-and-observability/` (Opik E2E RAG evaluation)
- **Pattern:** Grounding verification for retrieval-augmented generation
- **Focus:** Ensuring responses are based on retrieved context

### Multi-Modal & Text Quality Rubrics
- **Source:** `generative-ai/gemini/evaluation/evaltask_approach/`
- **Patterns:** Pointwise (single response) and Pairwise (comparison) evaluation
- **Use Cases:** Instruction following, text quality, hallucination detection

---

## Version History

- **v1.3.0** (March 2026) — Improved sub-agent prompts with structured reasoning, confidence scoring, edge case detection, and richer aggregation analysis
- **v1.2.0** (March 2026) — Multi-agent sequential evaluation for consensus-based verdicts, improved confidence scoring
- **v1.1.0** (March 2026) — Added rubric-based evaluation pattern (primary), documented local repo sources
- **v1.0.0** (March 2026) — Initial agent-native evaluation framework

