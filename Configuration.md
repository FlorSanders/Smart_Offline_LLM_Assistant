# Configuration Guide

Several aspects of the voice assistant can be configured by editing the [`config.json`](./config.json) file.

## Microphone Stream

- `mic_chunk`: Microphone stream chunk size.
- `mic_rate`: The sample rate used for the microphone input.
- `mic_from_file`: Feed sound from a `.wav` file rather than an actual mic input (used for testing).
  - NOTE: A wav file recording in the correct format can be made using the `test_record.py` script.
- `mic_file_path`: The `.wav` file to be used in case `mic_from_file` is set to `true`.

## Wakeword Algorithm

The wakeword algorithm in this project is powered by [openWakeWord](https://github.com/dscripka/openWakeWord).

- `wakeword_model_path`: Wakeword model weights path.
- `wakeword_download_model`: Automatically download model weights to `wakeword_model_path` (works for [known models](https://github.com/dscripka/openWakeWord/blob/main/openwakeword/__init__.py)).
- `wakeword_threshold`: Confidence level required for wakeword detection.
- `wakeword_sound`: Path to wakeword detection chime sound `.wav` file.
  - NOTE: A collection of notification sounds is availables in the [assets/sounds](./assets/sounds/) directory.

## Automatic Speech Recognition

This project aims to support multiple ASR engines.  
Their configuration options are listed below.

- `asr_model`: Name of the ASR model (supported values listed at the end of [asr.py](./pipeline/asr.py)).
- `asr_model_dir`: ASR model weights directory.
- `asr_download_model`: Automatically download model weights to `asr_model_dir`.

## Text-to-Speech

This project aims to support multiple TTS engines.  
Their configuration options are listed below.

- `tts_model`: Name of the TTS model (support values listed at the end of [tts.py](./pipeline/tts.py)).
- `tts_model_dir`: TTS model weihgts directory.
- `tts_download_model`: Automatically download model weights to `tts_model_dir`.
- `tts_voice`: Which voice to use for synthesis (if model has multiple options).
- `tts_file`: Temporary wav file to store the synthesized audio in.
