import typer
import pyaudio
import numpy as np
from pipeline.utils import get_config, get_logger
from pipeline.microphone import Microphone


def main(config_path: str = "./config.json", log_level: str = "DEBUG"):
    """
    Local-First LLM Voice Assistant - Main Script
    ---
    Args:
    - config_path (default = "./config.json"): Configuration file path
    - log_level (default = "DEBUG"): Logger level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """

    # Initialize program
    config = get_config(config_path)
    logger = get_logger(log_level=log_level)
    logger.info("Program Initialized")

    # Initialize microphone
    mic = Microphone(config)
    mic.open()
    try:
        chunk = True
        while np.any(chunk):
            chunk = mic.read_chunk()
    finally:
        logger.info("Closing Program")
        mic.close()

    return 0


if __name__ == "__main__":
    typer.run(main)
