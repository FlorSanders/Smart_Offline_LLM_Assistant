import typer
import os
import sys

# Add main dir to system path
main_dir = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
sys.path.append(main_dir)
from pipeline.asr import ASR  # ASR first (bug fix)
from pipeline.utils import get_config, get_logger
from pipeline.microphone import Microphone


def main(
    config_path: str = os.path.join(main_dir, "config.json"),
    log_level: str = "DEBUG",
):
    """
    Audio transcription test script
    """

    # Initialize program
    config = get_config(config_path)
    logger = get_logger(log_level=log_level)
    logger.info("Program Initialized")

    # Initialize microphone
    mic = Microphone(config)
    mic.open()

    # Transcribe audio
    asr = ASR(config, mic)

    result = asr.transcribe()
    print(result)

    return 0


if __name__ == "__main__":
    typer.run(main)
