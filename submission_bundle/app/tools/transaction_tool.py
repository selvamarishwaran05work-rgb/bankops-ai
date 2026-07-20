from app.tools.base_tool import BaseTool


class TransactionTool(BaseTool):

    @property
    def definition(self):
        return {
            "name": "get_customer_transactions",
            "description": "Returns recent customer transactions.",
            "when_to_use": [
                "Transaction dispute",
                "Duplicate debit",
                "Fraud review",
                "Chargeback investigation"
            ],
            "inputs": {
                "customer_id": "string"
            }
        }

    @property
    def name(self):
        return "get_customer_transactions"

    @property
    def description(self):
        return (
            "Returns recent customer transactions."
        )
    
    @property
    def input_schema(self):
        return {
            "customer_id": "string"
        }
    
    def execute(self, customer_id):

        return [
            {
                "merchant": "Amazon",
                "amount": 2500,
                "date": "2026-07-19"
            },
            {
                "merchant": "Amazon",
                "amount": 2500,
                "date": "2026-07-19"
            },
            {
                "merchant": "Swiggy",
                "amount": 480,
                "date": "2026-07-18"
            }
        ]