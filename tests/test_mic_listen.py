import os
import sys
import whisper
import numpy as np

# Add main dir to system path
main_dir = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
sys.path.append(main_dir)
from pipeline.utils import get_config, get_logger
from pipeline.microphone import Microphone

logger = get_logger("DEBUG")
mic = Microphone(
    {
        "mic_chunk": 1280,
        "mic_rate": 16000,
        "mic_from_file": False,
        "mic_file_path": "./microphone.wav",
    }
)

audio = mic.listen_until_silence(
    volume_threshold=0.25,
    silence_cutoff_length=10,
    verbose=True,
)
print(len(audio))
