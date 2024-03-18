import time
import typer
import pyaudio
import numpy as np
from pipeline.utils import get_config, get_logger
from pipeline.microphone import Microphone
from pipeline.tts import TTS


def main(config_path: str = "./config.json", log_level: str = "DEBUG"):
    """
    Text-to-speech test script
    """

    # Initialize program
    config = get_config(config_path)
    logger = get_logger(log_level=log_level)
    logger.info("Program Initialized")

    # Intialize tts
    tts = TTS(config)

    # Speak
    text = "Hello world!"
    tts.speak(text)


if __name__ == "__main__":
    typer.run(main)
