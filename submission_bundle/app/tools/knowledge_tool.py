from app.tools.base_tool import BaseTool
from app.services.knowledge_service import knowledge_service


class SearchBankPolicyTool(BaseTool):

    @property
    def definition(self):
        return {
            "name": "search_bank_policy",
            "description": (
                "Search the enterprise banking knowledge base for "
                "banking policies, investigation procedures, "
                "fraud guidelines, AML rules, KYC procedures, "
                "chargeback policies and operational manuals."
            ),
            "when_to_use": [
                "Fraud",
                "Duplicate debit",
                "Chargeback",
                "AML",
                "KYC",
                "Transaction disputes",
                "Compliance",
                "Banking procedures"
            ],
            "inputs": {
                "query": "Customer issue or investigation topic"
            }
        }

    def execute(self, query):
        return knowledge_service.search(query)


tool = SearchBankPolicyTool()