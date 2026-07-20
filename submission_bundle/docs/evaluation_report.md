# Evaluation Report

## Prompt comparison
The agent was tested with three prompt strategies against the same evaluation set.

| Prompt variant | Output quality | Strengths | Weaknesses |
| --- | --- | --- | --- |
| Baseline | Generic and shallow | Fast | Missed tool selection and lacked detail |
| Structured | More organized and actionable | Better plan formatting | Still occasional tool misrouting |
| Adaptive | Best balance of detail and grounding | Better reasoning, explicit tool use, more context-aware | Slightly slower and more verbose |

## Failure case and root cause
Failure case: the planner sometimes produced an invalid JSON plan or selected the wrong tool when the request was ambiguous.

Root cause:
- The prompt did not strongly constrain tool selection.
- The system lacked a resilient fallback when the LLM returned malformed output.

Fix:
- Added stronger tool-selection instructions and enforced a structured plan schema.
- Added a graceful fallback path and explicit logging for malformed responses.

## Before/after proof
Before:
- Plans were often too generic and inconsistent.
- Tool selection was not reliably grounded in the request.

After:
- The planner produces a more detailed plan, uses tools more appropriately, and surfaces evidence in the UI.

## Quality metrics
- Plan clarity: improved from weak to strong
- Tool grounding: improved through explicit tool definitions and prompting
- Resume reliability: verified through thread-state persistence tests
- Safety: refusals and escalation guidance are surfaced for unsupported requests
