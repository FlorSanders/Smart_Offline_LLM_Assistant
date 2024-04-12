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
from pipeline.tts import TTS


def main(
    config_path: str = os.path.join(main_dir, "config.json"),
    log_level: str = "DEBUG",
):
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
    text = "The current temperature in Halle, Belgium is 13.1°C with a relative humidity of 92% and a wind speed of 6.9 km/h."
    tts.speak(text)


if __name__ == "__main__":
    typer.run(main)
