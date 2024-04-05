import openai
import requests
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
        self.provider = config.get("llm_provider")

        # Initialize model
        self.model = providers[self.provider]["class"](config)

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
        self.base_url = config.get("llm_provider_url")
        self.model_name = config.get("llm_model")
        self.system_message = config.get("llm_system_message")

    def __call__(self, prompt):
        raise NotImplementedError("__call__() is not implemented in base class")


class OpenAIModel(LLMModel):
    def __init__(self, config):
        super().__init__(config)

        # Load OpenAI API key
        load_dotenv()
        self.client = openai.Client(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=self.base_url,
        )

    def __call__(self, prompt):
        messages = [
            {"role": "system", "content": self.system_message},
            {"role": "user", "content": prompt},
        ]
        self.logger.debug("Calling OpenAI API")
        chat = self.client.chat.completions.create(
            model=self.model_name, messages=messages
        )
        response_text = chat.choices[0].message.content
        self.logger.debug(f"OpenAI API response: {response_text}")
        return response_text


class LlamaEdgeModel(LLMModel):
    def __init__(self, config):
        super().__init__(config)
        # Default base url for LLamaEdge
        if self.base_url is None:
            self.base_url = "http://localhost:8080/v1"

    def __call__(self, prompt):
        # Construct messages
        messages = [
            {"role": "system", "content": self.system_message},
            {"role": "user", "content": prompt},
        ]

        # Perform API call
        self.logger.debug("Calling Llama Edge API")
        response = requests.post(
            f"{self.base_url}/chat/completions",
            json={
                "messages": messages,
                "model": self.model_name,
            },
            headers={"Content-Type": "application/json"},
        )

        # Confirm response success
        if response.status_code != 200:
            raise Exception(f"Error calling API: {response.text}")

        # Parse response
        response_body = response.json()
        response_text = response_body["choices"][0]["message"]["content"]
        self.logger.debug(f"API response {response_text}")

        return response_text


providers = {
    "openai": {
        "class": OpenAIModel,
    },
    "llama-edge": {
        "class": LlamaEdgeModel,
    },
}
