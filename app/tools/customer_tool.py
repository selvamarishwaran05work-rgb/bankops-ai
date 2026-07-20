from app.tools.base_tool import BaseTool


class CustomerTool(BaseTool):

    @property
    def definition(self):
        return {
            "name": "get_customer_profile",
            "description": "Returns customer profile.",
            "when_to_use": [
                "Customer profile lookup",
                "Customer onboarding",
                "Customer risk review"
            ],
            "inputs": {
                "customer_id": "string"
            }
        }

    @property
    def name(self):
        return "get_customer_profile"

    @property
    def description(self):
        return (
            "Returns customer profile."
        )

    @property
    def input_schema(self):
        return {
            "customer_id": "string"
        }
    
    def execute(self, customer_id):

        return {
            "customer_id": customer_id,
            "segment": "Premium",
            "risk": "Low"
        }