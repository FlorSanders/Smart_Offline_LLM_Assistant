import typer
from pipeline.utils import get_config, get_logger
from pipeline.microphone import Microphone
from pipeline.asr import ASR


def main(
    config_path: str = "./config.json",
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
    mic = Microphone(config)
    mic.open()

    # Transcribe audio
    asr = ASR(config, mic)

    result = asr.transcribe()
    print(result)

    return 0


if __name__ == "__main__":
    typer.run(main)
