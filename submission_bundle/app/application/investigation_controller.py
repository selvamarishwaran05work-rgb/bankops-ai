from app.capabilities.investigation_capability import InvestigationCapability


class InvestigationController:

    def __init__(self):
        self.capability = InvestigationCapability()

    def investigate(self, request):
        return self.capability.investigate(request)