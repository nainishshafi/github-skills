# Evaluation Approaches

Agent-native evaluation strategies using Claude as the built-in judge. No external APIs or script execution.

---

## Agent-Native Direct Evaluation

**How it works:** The agent evaluates responses using its internal reasoning within the conversation context.

**Strengths:**
- No external services or API calls
- Immediate results
- Full transparency (reasoning visible)
- Easy to customize
- No configuration needed

**Best for:**
- Quick evaluations in conversations
- Interactive refinement
- Custom criteria
- On-demand assessment

---

## Pattern 1: Single Response Scoring

Direct scoring without external calls.

**Example:**
```
You: "Rate this 1-5: {response}"
Agent: [Internal reasoning] Score: 4/5
```

---

## Pattern 2: Comparison Without Script

Head-to-head evaluation within agent context.

**Example:**
```
You: "Compare A and B"
Agent: [Internal reasoning] Winner: A
```

---

## Pattern 3: Hallucination Check

Context-based fact verification within agent.

**Example:**
```
You: "Check facts:
Context: Earth orbits Sun
Response: Earth orbits Sun, Moon orbits Mars"
Agent: [Reasoning] Hallucination found: Mars claim
```

---

## When to Use Agent-Native Evaluation

| Scenario | Approach |
|----------|----------|
| Quick comparison | Agent native |
| Real-time feedback | Agent native |
| Custom evaluation | Agent native |
| Transparent reasoning | Agent native |
| Interactive refinement | Agent native |

**All evaluation happens within the agent. No scripts, APIs, or external services needed.**



