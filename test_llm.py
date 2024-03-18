import time
import typer
import pyaudio
import numpy as np
from pipeline.utils import get_config, get_logger
from pipeline.microphone import Microphone
from pipeline.llm import LLM


def main(config_path: str = "./config.json", log_level: str = "DEBUG"):
    """
    LLM Interaction test script
    """

    # Initialize program
    config = get_config(config_path)
    logger = get_logger(log_level=log_level)
    logger.info("Program Initialized")

    # Intialize tts
    llm = LLM(config)

    # LLM processing
    prompt = "what is the weather today?"
    response = llm(prompt)


if __name__ == "__main__":
    typer.run(main)
