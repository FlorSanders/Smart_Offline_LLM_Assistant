import time
import typer
import pyaudio
import numpy as np
import os
import sys

# Add main dir to system path
main_dir = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
sys.path.append(main_dir)
from pipeline.utils import get_config, get_logger
from pipeline.microphone import Microphone
from pipeline.llm import LLM


def main(
    config_path: str = os.path.join(main_dir, "config.json"),
    log_level: str = "DEBUG",
):
    """
    LLM Interaction test script
    """

    # Initialize program
    config = get_config(config_path)
    logger = get_logger(log_level=log_level)
    logger.info("Program Initialized")

    # Intialize llm
    llm = LLM(config)

    # LLM processing
    prompt = "What is your name?"
    response = llm(prompt)
    print(response)


if __name__ == "__main__":
    typer.run(main)
