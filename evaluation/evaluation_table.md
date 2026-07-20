# Evaluation Table for BankOps AI

## Summary Table

| Evaluation Area | What to Measure | Score (1-5) | Evidence / Notes |
|---|---|---:|---|
| End-to-End Investigation Quality | Whether the assistant resolves the user issue clearly and usefully | 4 | Strong reasoning and relevant recommendation, but still depends on tool availability and model quality |
| Planner Quality | Whether the plan is relevant, structured, and efficient | 4 | Good plan structure with appropriate tool selection in most cases |
| Tool Use and Evidence Grounding | Whether tools are used correctly and outputs support the response | 3 | Tool outputs are useful, but evidence grounding can be improved further |
| Conversation Resume and Persistence | Whether saved conversations resume correctly and preserve context | 5 | Thread-level checkpointing and resume behavior are implemented successfully |
| Adaptive Feedback Learning | Whether feedback improves later responses | 4 | Feedback comments are captured and influence adaptive prompting |
| Safety and Escalation | Whether the system behaves safely and escalates when needed | 4 | Safe behavior is present, though escalation logic should remain explicit in production |
| User Experience | Whether the UI feels intuitive and conversational | 4 | The dashboard and resume flow are functional and polished |

## Suggested Interpretation
- 5 = Excellent
- 4 = Good
- 3 = Acceptable
- 2 = Weak
- 1 = Poor

## Example Scoring Notes
- Resume and persistence: 5/5 because the system successfully restores prior threads and continues from saved checkpoints.
- Tool use: 3/5 because the solution is functional but still depends on accurate tool outputs and tool selection quality.
- Safety: 4/5 because the system is cautious, but real banking use cases would require stronger guardrails and escalation logic.
