# Local-First LLM Voice Assistant with Tool Access

## Setup

In order to install the dependencies, initiate a conda environment from the `environment.yml` file.

```bash
conda env create -f environment.yml
```

If changes are made, the environment can be exported using the provided script.

```bash
bash export-environment.sh
```

In case you plan to use [OpenAI](https://openai.com/) GPT models as your LLM backend, you have to create a `.env` file with your [API key](https://platform.openai.com/api-keys).

```bash
OPENAI_API_KEY=YOUR-KEY
```

## Usage

The voice assistant lives in the main script.  
It can be started using a CLI interface.

```bash
 Usage: main.py [OPTIONS]

 Local-First LLM Voice Assistant

╭─ Options ───────────────────────────────────────────────────╮
│ --config-path        TEXT  [default: ./config.json]         │
│ --log-level          TEXT  [default: INFO]                  │
│ --help                     Show this message and exit.      │
╰─────────────────────────────────────────────────────────────╯
```

The voice assistant can be configured by editing the `config.json` file.  
Check out the [Configuration Guide](./Configuration.md) for more details.

## Architecture

The pipeline that powers the voice assistant stands on the shoulders of giants:

1. CLI Tool built on [Typer](https://github.com/tiangolo/typer)
2. Wakeword Detection with [openWakeWord](https://github.com/dscripka/openWakeWord)
3. Automatic Speech Recognition / Speech-to-Text with:
   - [Vosk](https://alphacephei.com/vosk/install)
4. Large Language Models, based on:
   - [OpenAI GPT](https://openai.com/gpt-4)
5. Speech Synthesis / Text-to-Speech with:
   - [Piper](https://github.com/rhasspy/piper)

## TODO

This repository is a work in progress, some things that remain to be done are:

- [ ] Automatic Speech Recognition Model, integrate multiple models:
  - [ ] [Distill Whisper Small](https://huggingface.co/distil-whisper/distil-small.en)
  - [ ] [Quartznet](https://catalog.ngc.nvidia.com/orgs/nvidia/models/quartznet15x5) -> [Jetson Voice Package](https://github.com/dusty-nv/jetson-voice?tab=readme-ov-file#automatic-speech-recognition-asr)
  - [ ] [Mozilla Deepspeech](https://deepspeech.readthedocs.io/en/r0.9/index.html)
  - [x] [Vosk](https://alphacephei.com/vosk/install)
- [ ] Speech to Text Model, Integrate multiple models:
  - [x] [Piper](https://github.com/rhasspy/piper)
  - [ ] [Microsoft Lightspeech](https://github.com/microsoft/NeuralSpeech/tree/master/LightSpeech)
  - [ ] [EfficientSpeech](https://github.com/roatienza/efficientspeech)
- [ ] Speaker Identification Model
- [ ] LLM Integration
- [ ] LLM Tool Learning
- [ ] Tool Access Integration

## Similar Projects

This project is supposed to be a proof-of-concept.  
There are a lot of interesting projects out there that are developed to a more mature point.  
Go check them out!

- [Leon](https://github.com/leon-ai/leon)
- [Mycroft](https://github.com/MycroftAI/mycroft-core)
- [rhasspy3](https://github.com/rhasspy/rhasspy3/)
- [and more...](https://github.com/topics/voice-assistants)
