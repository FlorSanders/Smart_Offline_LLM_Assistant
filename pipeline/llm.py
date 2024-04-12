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
        """
        Initialize the LLM
        ---
        Args:
        - config: Configuration dictionary
        """

        # Logger
        self.logger = get_logger()
        self.logger.debug("Configuring LLM")

        # Config
        self.provider = config.get("llm_provider")

        # Initialize model
        self.model = providers[self.provider]["class"](config)

    def __call__(self, prompt, system_prompt=None):
        """
        Prompt the LLM
        ---
        Args:
        - prompt: Prompt to send to the LLM
        - system_prompt: System prompt to send to the LLM

        Returns:
        - response: Response from the LLM
        """

        self.logger.debug(f"Prompting LLM")
        self.logger.debug(f"Prompt: {prompt}")
        if system_prompt is not None:
            self.logger.debug(f"System prompt: {system_prompt}")

        response = self.model(prompt, system_prompt=system_prompt)
        self.logger.debug(f"LLM response: {response}")
        return response


class LLMModel:
    def __init__(self, config):
        """
        Initialize the LLM model
        ---
        Args:
        - config: Configuration dictionary
        """

        # Logger
        self.logger = get_logger()
        self.logger.debug("Configuring LLM model")

        # Config
        self.config = config
        self.base_url = config.get("llm_provider_url")
        self.model_name = config.get("llm_model")
        self.system_message = config.get("llm_system_message")

    def __call__(self, prompt):
        """
        Perform inference with the LLM model
        ---
        Args:
        - prompt: Prompt to send to the LLM model

        Returns:
        - response: Response from the LLM model
        """

        raise NotImplementedError("__call__() is not implemented in base class")


class OpenAIModel(LLMModel):
    """
    OpenAIModel interfaces with OpenAI's large language model
    ---
    NOTE: It requires an OpenAI API key to be set in the environment
    """

    def __init__(self, config):
        super().__init__(config)

        # Load OpenAI API key
        load_dotenv()
        self.client = openai.Client(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=self.base_url,
        )

    def __call__(self, prompt, system_prompt=None):
        # Default system prompt
        if system_prompt is None:
            system_prompt = self.system_message

        # Construct messages
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]

        # Call API
        self.logger.debug("Calling OpenAI API")
        chat = self.client.chat.completions.create(
            model=self.model_name, messages=messages
        )

        # Parse response
        response_text = chat.choices[0].message.content

        return response_text


class LlamaEdgeModel(LLMModel):
    """
    LlamaEdgeModel interfaces with LlamaEdge's large language model
    ---
    NOTE: It requires a LlamaEdge instance running on the configured IP address
    """

    def __init__(self, config):
        super().__init__(config)
        # Default base url for LLamaEdge
        if self.base_url is None:
            self.base_url = "http://localhost:8080/v1"

    def __call__(self, prompt, system_prompt=None):
        # Default system prompt
        if system_prompt is None:
            system_prompt = self.system_message

        # Construct messages
        messages = [
            {"role": "system", "content": system_prompt},
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

        return response_text


providers = {
    "openai": {
        "class": OpenAIModel,
    },
    "llama-edge": {
        "class": LlamaEdgeModel,
    },
}
