import json


class ToolPromptBuilder:

    def build(self, tool_definitions):

        prompt = """
Available Enterprise Tools

The following tools are available.

Only choose from these tools.

"""

        for tool in tool_definitions:

            prompt += f"""

----------------------------------------------------

Tool Name

{tool["name"]}

Description

{tool["description"]}

When To Use

{json.dumps(tool["when_to_use"], indent=2)}

Inputs

{json.dumps(tool["inputs"], indent=2)}

"""

        return prompt


tool_prompt_builder = ToolPromptBuilder()