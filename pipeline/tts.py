import os
import wave
from urllib.request import urlretrieve
from piper.voice import PiperVoice
from .utils import get_logger
from .audio import play_wave_file


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

    def speak(self, text):
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
        play_wave_file(self.file)
        os.remove(self.file)


models = {
    "piper": {
        "class": PiperModel,
        "path": "piper",
        "url": lambda voice: f"https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/{voice}/low/en_US-{voice}-low.onnx",
    }  # Supported voices: https://huggingface.co/rhasspy/piper-voices/tree/main/en/en_US (only low variants!)
}
