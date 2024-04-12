import json
import re
from .utils import get_logger
from .tools import tools, ToolError
from .llm import LLM


class ToolLLM:
    def __init__(
        self,
        config: dict,
        llm: LLM,
        tool_selection: list = list(tools.keys()),
    ):
        # Initialize logger
        self.logger = get_logger()

        # Save arguments
        self.config = config
        self.llm = llm
        self.tool_selection = tool_selection
        if self.tool_selection is None:
            self.tool_selection = list(tools.keys())

        # Initialize tools
        self.tools = {}
        for label in self.tool_selection:
            self.tools[label] = tools[label]()

        # Generate tool prompt
        self.tools_prompt = self._get_tools_prompt()

    def _get_tools_prompt(self):
        tools_prompt = "Here are the tools you can use:\n"
        for label in self.tool_selection:
            tools_prompt += f"- {label}: {self.tools[label]}\n"
        tools_prompt += "You MUST always use one of the tools.\n"
        tools_prompt += 'Answers MUST be formatted in JSON format with "tool": name-of-tool and "arg": arg-value keys'
        tools_prompt += "\n---\n"
        return tools_prompt

    def _parse_llm_result(self, result):
        # Extract JSON string from LLM reply
        pattern = "\{(?:[^{}]|)*\}"
        matches = re.findall(pattern, result)
        assert len(matches), "Response must be in JSON format."

        # Parse JSON string into a dictionary
        result = json.loads(matches[0])
        tool_name = result.get("tool", "")
        tool_arg = result.get("arg", "")

        # Perform assertions
        assert (
            isinstance(tool_arg, str) and len(tool_arg) > 0
        ), f"Tool argument must be a string of non-zero length."
        assert tool_name in self.tools, f"Unknown tool {tool_name}"

        return tool_name, tool_arg

    def __call__(self, prompt: str, max_iterations: int = 5) -> str:
        # Keep track of response, context & whether we are finished
        response = ""
        context = ""
        initial_prompt = prompt

        # Prompt the LLM until we have a final response
        for iteration in range(max_iterations):
            try:
                # Build system prompt
                prompt = f"{self.llm.model.system_message}\n---\n{self.tools_prompt}"
                if len(context) > 0:
                    prompt += (
                        f"By using the tools you have obtained this information:\n"
                    )
                    prompt += f"{context}"
                    prompt += 'Once you have enough information, make use of the "answer" tool to provide a response to the user.'
                    prompt += "\n---\n"
                # Add actual prompt
                prompt += initial_prompt

                # Prompt LLM
                result = self.llm(prompt)

                # Parse LLM response
                try:
                    tool_name, tool_arg = self._parse_llm_result(result)
                # Catch Exceptions and re-prompt LLM
                except AssertionError as err:
                    warning_message = f"{err}"
                    context += f"WARNING: {warning_message}\n"
                    self.logger.warning(warning_message)
                    continue
                except json.JSONDecodeError as err:
                    warning_message = "Response must be in valid JSON format."
                    context += f"WARNING: {warning_message}\n"
                    self.logger.warning(warning_message)
                    continue

                # Check if we are done
                if tool_name == "answer":
                    response = tool_arg
                    break

                # Run tool
                try:
                    tool_result = self.tools[tool_name](tool_arg)
                    context += f'Tool "{tool_name}" with argument "{tool_arg}" returned "{tool_result}"\n'
                except ToolError as err:
                    warning_message = f'Tool "{tool_name}" raised an error: {err}'
                    context += f"WARNING: {warning_message}\n"
                    self.logger.warning(warning_message)
                    continue

            except Exception as e:
                print(e)
                raise Exception(e)
        else:  # Loop did not break
            raise ValueError(f"Max iterations ({max_iterations}) reached.")

        return response
