from app.capabilities.workflow_provider import WorkflowProvider


class InvestigationCapability:

    def __init__(self):
        self.workflow = WorkflowProvider.get_workflow()

    def investigate(self, request):
        return self.workflow.execute(request)