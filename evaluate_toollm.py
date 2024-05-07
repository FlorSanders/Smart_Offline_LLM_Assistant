from pipeline.asr import ASR  # ASR first (bug fix)
from pipeline.wakeword import Wakeword
from pipeline.utils import get_logger, get_config, name
from pipeline.audio import play_wave_file
from pipeline.microphone import Microphone
from pipeline.llm import LLM
from pipeline.toolllm import ToolLLM
from pipeline.tts import TTS
import time
import os
import logging
import typer


def evaluate_toollm(
    llm_provider="llama-edge",
    llm_model="Meta-Llama-3-8B-Instruct",
    llm_provider_url=None,
    log_level="INFO",
):
    """
    ToolLLM Task Evaluation
    ---
    Args:
    - llm_provider: Provider of the LLM
    - llm_model: Model of the LLM
    - log_level: Level of logs to be reported
    """

    # Logger
    logger = get_logger(log_level)

    # Construct config
    config = {
        "llm_provider": llm_provider,
        "llm_provider_url": llm_provider_url,
        "llm_model": llm_model,
        "llm_skip": False,
        "llm_use_tools": True,
        "llm_tools": None,
        "llm_system_message": "Your name is Sola, you are a helpful voice assistant. Keep responses short.",
    }

    # Initialize ToolLLM
    llm_model = LLM(config)
    llm = ToolLLM(config, llm_model, config["llm_tools"])

    # Tasks
    task_prompts = [
        # Simple instructions not requiring tool execution
        "What is your name?",
        "What can you help me with?",
        "Write me a poem about the tools you have access to.",
        # Simple questions requiring one tool
        "What is the current weather in Columbia University, NYC?",
        "What is fifty seven multiplied by three hundred and twenty one minus four?",
        "In what city did the 2020 olympic games take place?",
        # More difficult questions requiring two tools
        "What is the current weather in the city where the 2020 olympic games took place?",
        "What is the sum of the current temperature and humidity at Columbia University?",
        "What is the product of all the numbers of the year when the Olympic Games were held in Beijjing?",
        # Difficult questions requiring all three tools, or two tools and creativity
        "Write a poem about the current weather in the city where the 2020 olympic games took place.",
        "What is the sum of the current temperature and humidity in the city where the 2020 olympic games took place?",
    ]

    # Evaluate task prompts
    for i, prompt in enumerate(task_prompts):
        logger.info(f"Evaluating task {i}:\n{prompt}")
        response = llm(prompt)
        logger.info(f"Response:\n{response}")


# Run evaluation
if __name__ == "__main__":
    typer.run(evaluate_toollm)
