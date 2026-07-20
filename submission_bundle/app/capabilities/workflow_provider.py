from app.config.settings import settings
from app.workflow.rule_based_workflow import RuleBasedWorkflow
from app.workflow.llm_workflow import LLMWorkflow


class WorkflowProvider:

    @staticmethod
    def get_workflow():

        engine = settings.workflow_engine.lower()

        if engine == "rule":
            return RuleBasedWorkflow()

        elif engine == "llm":
            return LLMWorkflow()

        raise ValueError(f"Unsupported workflow engine: {engine}")