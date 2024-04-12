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

- `asr_model`: Name of the ASR model (supported values: `vosk`, `coqui`, `whisper`).
- `asr_model_dir`: ASR model weights directory.
- `asr_download_model`: Automatically download model weights to `asr_model_dir`.
- `asr_done_sound`: Path to end of ASR chime sound `.wav` file.
  - NOTE: A collection of notification sounds is availables in the [assets/sounds](./assets/sounds/) directory.

## Large Language Model

This project aims to support interfacing with multiple LLMs.
Their configuration options are listed below:

- `llm_provider`: LLM Service Provider (supported values: `openai`, `llamaedge`)
- `llm_provider_url`: To overwrite the `base_url` to which api calls should be made.
- `llm_model`: Name of the LLM model
  - `openai`: `gpt-3.5-turbo`, `gpt-4`
  - `llamaedge`: self-hosted llama-based model ([options](https://github.com/LlamaEdge/LlamaEdge/blob/main/models.md), e.g. `TinyLlama-1.1B-Chat-v1.0`)
- `llm_system_message`: System message sent to the LLM.
- `llm_use_tools`: Whether to use provide tool access to the LLM or not.
- `llm_tools`: What tools to have the LLM access. If set to default value `null`, access to all tools is enabled.
- `llm_skip`: Whether to skip the LLM altogether (used for testing).

## Text-to-Speech

This project aims to support multiple TTS engines.  
Their configuration options are listed below.

- `tts_model`: Name of the TTS model (supported values: `piper`, `coqui`, `mimic3`).
- `tts_voice`: Which voice to use for synthesis.
  - `piper`: `amy`, `danny`, `kathleen`, `lessac`, `ryan`
  - `coqui`: `tts_models/eng/fairseq/vits` (with [bug fix](https://github.com/eginhard/coqui-tts/pull/11/files/b064a57b2b97f019b5d5ccac8456169654e35641)), `tts_models/en/ljspeech/speedy-speech`, `tts_models/en/ljspeech/glow-tts`
  - `mimic3`: `en_US/cmu-arctic_low`, `en_US/hifi-tts_low`, `en_US/ljspeech_low`, `en_US/m-ailabs_low`, `en_US/vctk_low`, `en_UK/apope_low`
- `tts_model_dir`: TTS model weihgts directory.
- `tts_download_model`: Automatically download model weights to `tts_model_dir`.
- `tts_file`: Temporary wav file to store the synthesized audio in.
