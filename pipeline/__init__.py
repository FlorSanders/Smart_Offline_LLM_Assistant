from .asr import ASR  # ASR first (bug fix)
from .wakeword import Wakeword
from .utils import get_logger, get_config
from .audio import play_wave_file
from .microphone import Microphone
from .llm import LLM
from .tts import TTS
import time
import os


def run_pipeline(config_path, log_level):
    """
    Local-First LLM Voice Assistant Pipeline
    ---
    Args:
    - config_path: Path to the configuration file
    - log_level: Level of logs to be reported
    """

    # Logger
    logger = get_logger(log_level=log_level)

    # Load configuration
    logger.debug("Loading Configuration")
    config = get_config(config_path)

    # Initialize pipeline models
    logger.debug("Initializing Assistant Pipeline")
    mic = Microphone(config)
    wakeword = Wakeword(config, mic)
    asr = ASR(config, mic)
    # TODO: switch out llm for tool-llm, with a plan-execute-summarize feedback loop
    if config["llm_skip"]:
        llm = None
    else:
        llm = LLM(config)
    tts = TTS(config)

    # Run pipeline
    logger.info("Running Assistant Pipeline")
    while True:
        # Detect wakeword
        wakeword_detected = wakeword.detect()

        # Handle wakeword detection
        if not wakeword_detected:
            logger.info("Wakeword detection exited, shutting down.")
            break

        # Play wakeword chime
        if os.path.exists(config["wakeword_sound"]):
            logger.debug("Playing wakeword chime")
            play_wave_file(config["wakeword_sound"])

        # Transcribe audio
        prompt = asr.transcribe()

        # Play done listening chime
        if os.path.exists(config["asr_done_sound"]):
            logger.debug("Playing TTS done chime")
            play_wave_file(config["asr_done_sound"])
            time.sleep(0.1)

        # Process prompt
        if config["llm_skip"]:
            response = prompt
        else:
            response = llm(prompt)

        # Speak response
        tts.speak(response)

        # Play TTS done chime
        logger.debug("Sleeping...")
        time.sleep(0.25)
