import typer
from pipeline.asr import ASR  # ASR first (bug fix)
from pipeline.utils import get_config, get_logger
from pipeline.microphone import Microphone


def main(
    config_path: str = "./config.json",
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
