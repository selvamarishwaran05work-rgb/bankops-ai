# BankOps AI Investigation Assistant

## Overview
This project implements a bank-operations investigation assistant with a multi-step workflow:
- baseline handling and structured investigation prompts
- LLM-based reasoning
- retrieval from a knowledge base
- tool usage for customer and transaction context
- checkpointed, resumable conversations
- feedback-driven adaptation

## Features
- Natural-language investigation intake
- Planner, tool, and responder workflow
- Persisted thread checkpoints for conversation resume
- Feedback tracking that influences later planning
- Safe, explainable output with escalation guidance

## Project structure
- streamlit_app.py: Streamlit UI
- main.py: local entry point
- app/: agent workflow, prompts, services, tools, graph nodes
- docs/: problem framing, demo script, evaluation report, engineering rationale
- tests/: regression and behavior tests

## Setup
1. Create and activate a Python environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set the required environment variables for your AI provider and vector store.

## Run locally
Start the UI with either of the following:
```bash
streamlit run streamlit_app.py
```
or
```bash
python main.py
```

## Verification
The project includes a regression test for resume/persistence behavior and a verification log in docs/artifacts/verification.log.

## Demo flow
1. Enter a customer ID and investigation request.
2. Submit the request to generate a plan and recommendation.
3. Review tool outputs and resume previous conversations from the sidebar.
4. Provide feedback to influence later adaptive behavior.
