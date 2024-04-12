from .asr import ASR  # ASR first (bug fix)
from .wakeword import Wakeword
from .utils import get_logger, get_config
from .audio import play_wave_file
from .microphone import Microphone
from .llm import LLM
from .toolllm import ToolLLM
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
    llm_skip = config["llm_skip"]
    llm_use_tools = config["llm_use_tools"]

    # Initialize voice pipeline models
    logger.debug("Initializing Assistant Pipeline")
    mic = Microphone(config)
    wakeword = Wakeword(config, mic)
    asr = ASR(config, mic)
    tts = TTS(config)

    # Initialize LLM / ToolLLM
    if llm_skip:
        # Skipping over LLM execution
        llm = None
    elif llm_use_tools:
        # LLM with Tool Usage
        llm_model = LLM(config)
        llm = ToolLLM(config, llm_model, config["llm_tools"])
    else:
        # Basic LLM
        llm = LLM(config)

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

        # Handle empty prompt
        if not len(prompt):
            time.sleep(0.25)
            continue

        # Process prompt
        if llm_skip:
            response = prompt
        else:
            response = llm(prompt)

        # Speak response
        tts.speak(response)

        # Play TTS done chime
        logger.debug("Sleeping...")
        time.sleep(0.25)
