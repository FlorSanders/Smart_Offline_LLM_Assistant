import openai
from dotenv import load_dotenv
from .utils import get_logger
import os


class LLM:
    """
    LLM implements large language model by selecting and configuring one of the supported models
    ---
    """

    def __init__(self, config):
        # Logger
        self.logger = get_logger()
        self.logger.debug("Configuring LLM")

        # Config
        self.model_config = models[config.get("llm_model")]
        self.model = self.model_config["class"](config)

    def __call__(self, prompt):
        self.logger.debug(f"Prompting LLM: {prompt}")
        response = self.model(prompt)
        self.logger.debug(f"LLM response: {response}")
        return response


class LLMModel:
    def __init__(self, config):
        # Logger
        self.logger = get_logger()
        self.logger.debug("Configuring LLM model")

        # Config
        self.config = config
        self.model_name = config.get("llm_model")
        self.model_config = models[self.model_name]
        self.system_message = config.get("llm_system_message")

    def __call__(self, prompt):
        raise NotImplementedError("__call__() is not implemented in base class")


class OpenAIModel(LLMModel):
    def __init__(self, config):
        super().__init__(config)

        # Load OpenAI API key
        load_dotenv()
        self.client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))

    def __call__(self, prompt):
        messages = [
            {"role": "system", "content": self.system_message},
            {"role": "user", "content": prompt},
        ]
        self.logger.debug("Calling OpenAI API")
        chat = self.client.chat.completions.create(
            model=self.model_name, messages=messages
        )
        self.logger.debug(f"OpenAI API response {chat}")
        response = chat.choices[0].message.content
        return response


models = {
    "gpt-3.5-turbo": {
        "class": OpenAIModel,
    },
    "gpt-4": {
        "class": OpenAIModel,
    },
}
