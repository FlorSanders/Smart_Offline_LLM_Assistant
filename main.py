import time
import typer
import pyaudio
import numpy as np
from pipeline.utils import get_config, get_logger
from pipeline.microphone import Microphone
from pipeline.wakeword import Wakeword


def main(config_path: str = "./config.json", log_level: str = "INFO"):
    """
    Local-First LLM Voice Assistant - Main Script
    ---
    Args:
    - config_path (default = "./config.json"): Configuration file path
    - log_level (default = "INFO"): Logger level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """

    # Initialize program
    config = get_config(config_path)
    logger = get_logger(log_level=log_level)
    logger.info("Program Initialized")

    # Initialize microphone
    mic = Microphone(config)

    # Initialize wakeword
    wakeword = Wakeword(config, mic)

    # Detect wakeword
    while True:
        # Detect wakeword
        wakeword_detected = wakeword.detect()

        # Handle wakeword detection
        if not wakeword_detected:
            logger.info("Wakeword detection exited, shutting down.")
            break

        # Sleep some time
        time.sleep(0.1)

    return 0


if __name__ == "__main__":
    typer.run(main)
