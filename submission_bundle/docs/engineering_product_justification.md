# Engineering and Product Justification

## Why this design
The solution follows an industry-style agent workflow: baseline agent, LLM integration, retrieval, tool use, memory, adaptation, and deployment readiness. This progression makes the system explainable and practical for real investigations rather than overly academic.

## Design choices
- Streamlit was chosen for a fast, user-friendly interface that lets investigators interact with the agent without needing a custom frontend.
- LangGraph provides a structured workflow for planning, tool use, and responding.
- Checkpointing and thread persistence make the system usable across sessions.
- Feedback collection creates a lightweight adaptation loop without requiring complex retraining.

## Safety approach
- The system avoids fabricating customer or policy details.
- Unsafe requests are handled with explicit safeguards and escalation guidance.
- Sensitive outputs are not exposed outside the approved workflow.

## Deployment assumptions
- The app can be run locally with the required Python dependencies.
- The environment requires the appropriate API keys for the LLM, embeddings, and vector store.
- In production, logging and monitoring should be extended with structured traces and error capture.
