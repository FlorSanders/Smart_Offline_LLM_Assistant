import typer
import pyaudio
from pipeline.utils import get_config, get_logger
from pipeline.microphone import Microphone


def main(
    duration: int = 5,
    config_path: str = "./config.json",
    log_level: str = "DEBUG",
):
    """
    Record audio from microphone and save it to a file
    ---
    Args:
    - duration (default = 5): Duration of recording in seconds
    - config_path (default = "./config.json"): Configuration file path
    - log_level (default = "DEBUG"): Logger level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
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
