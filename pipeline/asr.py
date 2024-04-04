import whisper
import os
import json
import vosk
import stt
import zipfile
import time
import numpy as np
from urllib.request import urlretrieve
from .utils import get_logger
from .microphone import Microphone

vosk.SetLogLevel(-1)


class ASR:
    """
    ASR implements speech-to-text by selecting and configuring one of the supported models
    ---
    """

    def __init__(self, config: dict, mic: Microphone):
        """
        Initialize ASR
        ---
        Args:
        - config: Dictionary containing configuration parameters.
        - mic: Microphone object.
        """

        # Logger
        self.logger = get_logger()
        self.logger.debug("Configuring ASR")

        # Microphone
        self.model_config = models[config.get("asr_model")]
        self.model = self.model_config["class"](config, mic)

    def transcribe(self):
        """
        Transcribe audio from microphone input
        ---
        Returns:
        - transcription: Transcribed text from microphone input
        """
        self.logger.debug("Transcribing audio")
        transcription = self.model.transcribe()
        self.logger.debug(transcription)
        return transcription


class ASRModel:
    """
    ASRModel wraps around multiple speech-to-text model with a uniform interface
    ---
    """

    def __init__(self, config: dict, mic: Microphone):
        """
        Initialize ASR Model
        ---
        Args:
        - config: Dictionary containing configuration parameters.
        - mic: Microphone object.
        """

        # Logger
        self.logger = get_logger()
        self.logger.debug("Configuring ASR Model")

        # Microphone
        self.mic = mic

        # Configuration
        self.model_config = models[config["asr_model"]]
        self.mic_rate = config.get("mic_rate")
        self.model_dir = os.path.join(config.get("asr_model_dir"), config["asr_model"])
        self.model_path = os.path.join(self.model_dir, self.model_config["path"])

        # Donwload model
        if config.get("asr_download_model", False):
            self.download_model()

        # Load model
        self.load_model()

    def download_model(self, url=None):
        """
        Download ASR model weights
        ---
        """

        # Return if model already exists
        if os.path.exists(self.model_path):
            self.logger.debug("Model already exists")
            return

        # Make sure model dir exists
        os.makedirs(self.model_dir, exist_ok=True)

        # Get model url
        model_url = self.model_config["url"] if url is None else url
        file_name = model_url.split("/")[-1]

        # Download file
        self.logger.info("Downloading ASR model...")
        urlretrieve(model_url, os.path.join(self.model_dir, file_name))

        # Unzip file
        if os.path.splitext(file_name)[-1] == ".zip":
            self.logger.info("Unzipping ASR model...")
            with zipfile.ZipFile(
                os.path.join(self.model_dir, file_name), "r"
            ) as zip_ref:
                zip_ref.extractall(self.model_dir)
        self.logger.info("ASR model downloaded")

    def load_model(self):
        """
        Load ASR Model
        ---
        """
        raise NotImplementedError("load_model() not implemented in base class")

    def transcribe(self):
        """
        Transcribe speech to text from microphone
        ---
        Returns:
        - transcription: Transcribed text from microphone input
        """
        raise NotImplementedError("transcribe() not implemented in base class")


class VoskModel(ASRModel):
    """
    Speech-to-text model based on Vosk library
    https://alphacephei.com/vosk/
    ---
    """

    def load_model(self):
        self.logger.debug("Loading ASR model")
        self.model = vosk.Model(model_path=self.model_path)
        self.recognizer = vosk.KaldiRecognizer(self.model, self.mic_rate)

    def transcribe(self):
        # Make sure microphone is open
        if not self.mic.is_open:
            self.logger.debug("Opening microphone.")
            self.mic.open()

        # Transcribe audio
        while True:
            data = self.mic.read_chunk()
            if len(data) == 0:
                break
            if self.recognizer.AcceptWaveform(data.tobytes()):
                # Parse transcription result
                transcription_result = self.recognizer.Result()

                # Check if result is useful
                if not transcription_result:
                    continue

                # Convert to text
                transcription_result = json.loads(transcription_result).get("text", "")

                # Return
                self.logger.info(f"Speech detected: {transcription_result}")
                return transcription_result


class CoquiModel(ASRModel):
    """
    Speech-to-text model based on CoquiSTT (formerly DeepSpeech) library
    https://stt.readthedocs.io/en/latest/index.html
    ---
    """

    def download_model(self, url=None):
        # Download scorer
        super().download_model(url=self.model_config["scorer_url"])
        # Download model
        super().download_model(url=url)

    def load_model(self):
        # Load model
        self.logger.debug("Loading ASR model")
        self.model = stt.Model(self.model_path)
        self.logger.debug("Loading ASR scorer")
        self.model.enableExternalScorer(
            os.path.join(self.model_dir, self.model_config["scorer_path"])
        )

    def transcribe(self):
        # Get audio
        self.logger.debug("Gathering audio.")
        audio = self.mic.listen_until_silence()

        # Perform transcription
        self.logger.debug("Transcribing.")
        stream_context = self.model.createStream()
        stream_context.feedAudioContent(audio)
        result = stream_context.finishStream()

        return result


class WhisperModel(ASRModel):
    def load_model(self):
        # Load model
        self.logger.debug("Loading ASR model")
        self.model = whisper.load_model(self.model_path)

    def transcribe(self):
        # Get audio
        self.logger.debug("Gathering audio.")
        audio = self.mic.listen_until_silence()
        audio = audio.astype(np.float32) / 32768.0

        # Perform transcription
        self.logger.debug("Transcribing.")
        result = self.model.transcribe(audio)

        # Return transcription
        return result.get("text", "")


# Supported models
models = {
    "vosk": {
        "class": VoskModel,
        "url": "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip",
        "path": "vosk-model-small-en-us-0.15",
    },
    "coqui": {
        "class": CoquiModel,
        "url": r"https://github.com/coqui-ai/STT-models/releases/download/english%2Fcoqui%2Fv1.0.0-large-vocab/model.tflite",
        "path": "model.tflite",
        "scorer_url": r"https://github.com/coqui-ai/STT-models/releases/download/english%2Fcoqui%2Fv1.0.0-large-vocab/large_vocabulary.scorer",
        "scorer_path": "large_vocabulary.scorer",
    },
    "whisper": {
        "class": WhisperModel,
        "url": r"https://openaipublic.azureedge.net/main/whisper/models/d3dd57d32accea0b295c96e26691aa14d8822fac7d9d27d5dc00b4ca2826dd03/tiny.en.pt",
        "path": "tiny.en.pt",
    },
}
