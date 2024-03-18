import time
import typer
import pyaudio
import numpy as np
from pipeline.utils import get_config, get_logger
from pipeline.microphone import Microphone
from pipeline.wakeword import Wakeword
from pipeline.audio import play_wave_file
from pipeline.asr import ASR
from pipeline.tts import TTS


def main(config_path: str = "./config.json", log_level: str = "INFO"):
    """
    Local-First LLM Voice Assistant
    """

    # Initialize program
    config = get_config(config_path)
    logger = get_logger(log_level=log_level)
    logger.info("Program Initialized")

    # Initialize microphone
    mic = Microphone(config)

    # Initialize wakeword
    wakeword = Wakeword(config, mic)

    # Initalize asr
    asr = ASR(config, mic)

    # Intialize tts
    tts = TTS(config)

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

        # Transcribe audio
        transcription = asr.transcribe()

        # Process transcription TODO
        response = transcription

        # Speak response
        tts.speak(response)

        # Sleep some time
        time.sleep(0.1)

    return 0


if __name__ == "__main__":
    typer.run(main)
