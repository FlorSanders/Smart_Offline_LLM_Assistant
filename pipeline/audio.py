import pyaudio
import wave


def play_wave_file(file_path, chunk=1024):
    """
    Plays a wave file
    ---
    Args:
    - file_path: Path to the wav file
    - chunk (default = 1024): Chunk size for reading the file
    """

    wave_file = wave.open(file_path, "rb")
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=audio.get_format_from_width(wave_file.getsampwidth()),
        channels=wave_file.getnchannels(),
        rate=wave_file.getframerate(),
        output=True,
    )
    data = wave_file.readframes(chunk)
    while data:
        stream.write(data)
        data = wave_file.readframes(chunk)
    stream.close()
    audio.terminate()
    wave_file.close()
