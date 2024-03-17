import os
import numpy as np
import openwakeword
from openwakeword import Model
from .utils import get_logger
from .microphone import Microphone

# Download models
openwakeword.utils.download_models(target_directory="./models/wakeword")


class Wakeword:
    """
    Wakeword algorithm analyzes audio chunks and detects keywords
    ---
    """

    def __init__(self, config: dict, mic: Microphone):
        # Logger
        self.logger = get_logger()
        self.logger.debug("Configurating Wakeword")

        # Microphone
        self.mic = mic

        # Configuration
        self.threshold = config.get("wakeword_threshold")
        self.model_path = config.get("wakeword_model_path")
        model_name, model_ext = os.path.splitext(os.path.basename(self.model_path))
        self.model_name = model_name
        self.framework = model_ext[1:]
        self.last_detected = False

        # Model
        self.model = Model(
            wakeword_models=[self.model_path], inference_framework=self.framework
        )

    def detect(self):
        """
        Detect wakeword in audio chunk
        ---
        Args:
        - mic: Microphone object
        ---
        Returns:
        - True if wakeword detected, False otherwise
        """

        # Make sure microphone is open
        if not self.mic.is_open:
            self.logger.debug("Opening microphone.")
            self.mic.open()

        # Log
        self.logger.debug("Detecting wakeword")

        while True:
            # Read audio chunk
            audio_chunk = self.mic.read_chunk()
            if not (np.any(audio_chunk) or len(audio_chunk)):
                self.logger.error("Audio chunk invalid.")
                self.last_detected = False
                self.mic.close()
                return False

            # Detect wakeword
            prediction = self.model.predict(audio_chunk)
            prediction_value = prediction[self.model_name]
            wakeword_detected = prediction_value > self.threshold

            # Debounce detection
            if wakeword_detected and not self.last_detected:
                self.logger.info("Wakeword detected!")
                self.last_detected = True
                return True

            # Update last detection
            self.last_detected = wakeword_detected