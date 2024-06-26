import os
import wave
import re
from urllib.request import urlretrieve
from piper.voice import PiperVoice
from num2words import num2words
import torch
from TTS.api import TTS as CoquiTTS
from mycroft_plugin_tts_mimic3 import Mimic3TTSPlugin
from .utils import get_logger
from .audio import play_wave_file

device = "cuda" if torch.cuda.is_available() else "cpu"


class TTS:
    """
    TTS implements speech-to-text by selecting and configuring one of the supported models
    ---
    """

    def __init__(self, config):
        """
        Initialize TTS
        ---
        Args:
        - config: Dictionary containing configuration parameters.
        """

        # Logger
        self.logger = get_logger()
        self.logger.debug("Configuring TTS")

        # Config
        self.model_config = models[config.get("tts_model")]
        self.model = self.model_config["class"](config)
        self.character_map = {
            "°": "degree",
            "%": "percent",
            "$": "dollar",
            "£": "pound",
            "€": "euro",
            "&": "and",
            "@": "at",
            "#": "hashtag",
            "*": "asterisk",
        }

    def _replace_numbers_with_words(self, text):
        """
        Replace numbers with words
        ---
        Args:
        - text: Text to be processed
        """

        # Find numbers
        matches = re.findall(r"(\d+\.{0,1}\d+)", text)

        # Replace all numbers
        for match in matches:
            text = text.replace(match, f" {num2words(float(match))} ")

        return text

    def _replace_special_characters_with_words(self, text):
        """
        Replace special characters with words
        ---
        Args:
        - text: Text to be processed
        """

        # Find special characters
        matches = re.findall(r"([^A-zÀ-ú\s,?;.:\/0-9])", text)

        # Replace known special characters
        for match in matches:
            if match in self.character_map:
                text = text.replace(match, f" {self.character_map[match]} ")
            else:
                self.logger.warning(f"Unknown special character: {match}")

        return text

    def speak(self, text):
        text = text.strip()
        if len(text) == 0:
            self.logger.warning("Empty text, skipping tts")
            return
        text = self._replace_numbers_with_words(text)
        text = self._replace_special_characters_with_words(text)
        self.logger.debug(f"Speaking text: {text}")
        self.model.speak(text)


class TTSModel:
    """
    TTSModel wraps around multiple text-to-speech models with a uniform interface
    ---
    """

    def __init__(self, config):
        """
        Initialize TTS Model
        ---
        Args:
        - config: Dictionary containing configuration parameters.
        """

        # Logger
        self.logger = get_logger()

        # Configuration
        self.config = config
        self.model_dir = config.get("tts_model_dir")
        self.voice = config.get("tts_voice")
        self.file = config.get("tts_file")
        self.model_config = models[config.get("tts_model")]
        self.model_path = os.path.join(
            self.model_dir, self.model_config["path"], self.voice
        )

        # Download model
        if config.get("tts_download_model", False):
            self.download_model()

        # Load model
        self.load_model()

    def download_model(self):
        """
        Download TTS model weights
        ---
        """

        raise NotImplementedError(
            "download_model() is not implemented in the base class"
        )

    def load_model(self):
        """
        Load TTS Model
        ---
        """

        raise NotImplementedError("load_model() is not implemented in the base class")

    def speak(self, text):
        """
        Synthesize speech from text and play on the speakers
        ---
        Args:
        - text: Text to be spoken
        """

        raise NotImplementedError("speak() is not implemented in the base class")

    def speak_file(self):
        """
        Play audio saved in file and remove file
        ---
        """
        if not os.path.exists(self.file):
            self.logger.error(f"File not found: {self.file}")
            return

        play_wave_file(self.file)
        os.remove(self.file)


class PiperModel(TTSModel):
    def download_model(self):
        # Return if model exists
        if os.path.exists(self.model_path):
            self.logger.debug("Model already exists")
            return

        # Construct url
        url_onnx = self.model_config["url"](self.voice)
        url_json = f"{url_onnx}.json"

        # Make sure model path exists
        os.makedirs(self.model_path)

        # Download model
        self.logger.info("Downloading TTS model...")
        urlretrieve(url_onnx, os.path.join(self.model_path, "model.onnx"))
        urlretrieve(url_json, os.path.join(self.model_path, "model.onnx.json"))
        self.logger.info("TTS model downloaded")

    def load_model(self):
        self.logger.debug("Loading TTS model")
        self.model = PiperVoice.load(os.path.join(self.model_path, "model.onnx"))

    def speak(self, text):
        with wave.open(self.file, "wb") as wav_file:
            self.model.synthesize(text, wav_file)
        self.speak_file()


class CoquiModel(TTSModel):
    """
    Text-to-speech model based on CoquiTTS
    https://docs.coqui.ai/en/latest/index.html
    ---
    """

    def download_model(self):
        pass

    def load_model(self):
        self.logger.debug(f"Loading TTS model (device={device})")
        # Set models directory using environment variable
        os.environ["TTS_HOME"] = os.path.join(self.model_dir, self.model_config["path"])
        # (Down)Load model
        self.model = CoquiTTS(self.voice).to(device)

    def speak(self, text):
        self.model.tts_to_file(text=text, file_path=self.file)
        self.speak_file()


class Mimic3TTS(TTSModel):
    """
    Text-to-speech model based on Mycroft/Mimic3
    https://github.com/MycroftAI/mimic3
    """

    def download_model(self):
        pass

    def load_model(self):
        self.logger.debug(f"Loading TTS model")
        # Model configuration
        voices_dir = os.path.join(self.model_dir, self.model_config["path"])
        model_config = {
            "voice": self.voice,
            "voices_directories": [voices_dir],
            "voices_download_dir": voices_dir,
            "no_download": not self.config.get("tts_download_model", False),
        }
        # (Down)Load model
        self.model = Mimic3TTSPlugin("en", model_config)

    def speak(self, text):
        self.model.get_tts(text, self.file)
        self.speak_file()


models = {
    "piper": {
        "class": PiperModel,
        "path": "piper",
        "url": lambda voice: f"https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/{voice}/low/en_US-{voice}-low.onnx",
    },  # Supported voices: https://huggingface.co/rhasspy/piper-voices/tree/main/en/en_US (only low variants!)
    "coqui": {
        "class": CoquiModel,
        "path": "coqui",
        "url": None,
    },  # Supported voices: https://docs.coqui.ai/en/latest/
    "mimic3": {
        "class": Mimic3TTS,
        "path": "mimic3",
        "url": None,
    },  # Supported voices: https://github.com/MycroftAI/mimic3-voices
}
