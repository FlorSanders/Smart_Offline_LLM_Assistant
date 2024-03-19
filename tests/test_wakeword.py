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
from pipeline.wakeword import Wakeword
from pipeline.audio import play_wave_file


def main(
    config_path: str = os.path.join(main_dir, "config.json"),
    log_level: str = "DEBUG",
):
    """
    Wakeword detection test script
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

        # Play wakeword chime
        logger.debug("Playing wakeword chime")
        play_wave_file(config["wakeword_sound"])

        # Sleep some time
        time.sleep(0.1)

    return 0


if __name__ == "__main__":
    typer.run(main)
