# Problem Framing: BankOps AI Investigation Assistant

## Persona and workflow
Primary persona: a bank operations investigator who handles customer disputes, fraud cases, and policy-related escalations. Their workflow is fast-paced and operational: they receive a customer issue, need to gather relevant context quickly, decide whether the case should be escalated, and produce an actionable recommendation.

## Problem to solve
Investigators often need to search policies, review customer and transaction context, and assemble a clear plan while under time pressure. Manual investigation is slow, inconsistent, and prone to missing key evidence. The agent should reduce friction by turning a natural-language report into a structured investigation workflow with planning, retrieval, tool usage, and a resumable conversation history.

## Inputs, outputs, constraints, and assumptions
Inputs:
- Customer ID
- Investigation request text
- Optional prior conversation/thread state

Outputs:
- Investigation plan
- Tool outputs
- Final recommendation
- Confidence and escalation signal
- Persisted conversation checkpoint

Constraints:
- Must be safe and explainable
- Must avoid fabricating policy or customer data
- Must provide clear evidence for tool use and recommendations
- Must support multi-turn, resumable sessions

Assumptions:
- The system can access a knowledge base and a limited set of operational tools
- The environment is configured with the relevant API keys and dependencies

## Example user questions
1. Why was a customer charged twice for the same transaction?
2. Review the policy for a disputed chargeback request.
3. Investigate suspicious activity for customer C100.
4. Should this case be escalated to compliance?
5. Resume my previous investigation for this customer.

## Success criteria
- The agent produces a clear plan and recommendation from a natural-language request.
- Retrieval and tool outputs are surfaced clearly to the user.
- The user can resume prior investigations from a persisted thread.
- Feedback can influence later behavior in a visible way.
- The system fails gracefully when services are unavailable.

## Known failure cases and edge scenarios
- Missing or invalid customer ID
- Retrieval returns no relevant context
- Tool execution fails or returns incomplete data
- User asks for an unsupported investigation action
- The LLM produces a malformed or non-JSON plan
- The service is temporarily unavailable

These cases are handled with structured fallbacks, explicit user-facing errors, and safe escalation guidance.
