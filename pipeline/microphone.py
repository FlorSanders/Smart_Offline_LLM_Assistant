import pyaudio
import wave
import numpy as np
from .utils import get_logger


class Microphone:
    """
    Microphone class interfaces with microphone or simulates microphone input from wav file
    ---
    """

    def __init__(
        self,
        config: dict,
    ):
        """
        Initialize microphone
        ---
        Args:
        - config Dictionary containing configuration parameters.
            - mic_chunk: Number of frames to read from microphone.
            - mic_rate: Microphone sample rate.
            - mic_from_file: If true, read from wav file.
            - mic_file_path: Path to wav file.
        """

        # Get logger
        self.logger = get_logger()
        self.logger.debug("Configuring Microphone")

        # Configuration
        self.format = pyaudio.paInt16
        self.channels = 1
        self.chunk = config.get("mic_chunk", 1280)
        self.rate = config.get("mic_rate", 16000)
        self.from_file = config.get("mic_from_file", False)
        self.file_path = config.get("mic_file_path", "")

        # Microphone stream
        self.audio = None
        self.stream = None

    @property
    def is_open(self):
        """
        Check if microphone is open
        ---
        Returns:
        - is_open: True if microphone is open, False otherwise.
        """
        return self.audio is not None and self.stream is not None

    def open(self):
        """
        Open microphone audio stream
        ---
        """

        # Log
        self.logger.debug("Starting microphone stream")

        # Open mic stream
        self.audio = pyaudio.PyAudio()
        if self.from_file:
            self.wav_file = wave.open(self.file_path, "rb")
            self.stream = self.audio.open(
                format=self.audio.get_format_from_width(self.wav_file.getsampwidth()),
                channels=self.wav_file.getnchannels(),
                rate=self.wav_file.getframerate(),
                output=True,
            )
        else:
            self.stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk,
            )

    def record(self, duration=30):
        """
        Record audio fragment to file
        ---
        Args:
        - duration (default = 30): Recording duration in seconds
        """
        with wave.open(self.file_path, "wb") as wav_file:
            wav_file.setnchannels(self.channels)
            wav_file.setsampwidth(self.audio.get_sample_size(self.format))
            wav_file.setframerate(self.rate)

            for _ in range(int(duration * self.rate / self.chunk)):
                data = self.stream.read(self.chunk)
                wav_file.writeframes(data)

    def read_chunk(self):
        """
        Read a chunk of data from the microphone
        ---
        Returns:
        - data: Audio chunk
        """
        # Read chunk from mic
        if self.from_file:
            data = self.wav_file.readframes(self.chunk)
        else:
            data = self.stream.read(self.chunk)

        # Parse to array
        data = np.frombuffer(data, dtype=np.int16)

        return data

    def close(self):
        """
        Close the microphone audio stream
        ---
        """

        # Log
        self.logger.debug("Stopping microphone stream")

        # Stop microphone stream
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        # Terminate audio process
        if self.audio:
            self.audio.terminate()
            self.audio = None
