import typer
import pyaudio
import os
import sys

# Add main dir to system path
main_dir = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
sys.path.append(main_dir)
from pipeline.utils import get_config, get_logger
from pipeline.microphone import Microphone


def main(
    duration: int = 5,
    config_path: str = os.path.join(main_dir, "config.json"),
    log_level: str = "DEBUG",
):
    """
    Record audio from microphone and save it to a file
    """

    # Initialize program
    config = get_config(config_path)
    logger = get_logger(log_level=log_level)
    logger.info("Program Initialized")

    # Initialize microphone
    config["mic_from_file"] = False  # make sure we record from microphone
    mic = Microphone(config)
    mic.open()
    logger.info("Start recording")
    mic.record(duration=duration)
    logger.info("Stop recording")
    mic.close()

    return 0


if __name__ == "__main__":
    typer.run(main)
