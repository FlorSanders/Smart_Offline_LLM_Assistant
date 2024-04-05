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

### OpenAI

To use [OpenAI](https://openai.com/) GPT models as your LLM backend, you have to create a `.env` file with your [API key](https://platform.openai.com/api-keys).

```bash
OPENAI_API_KEY=YOUR-KEY
```

### Mimic3

To use [MycroftAI/mimic3](https://github.com/MycroftAI/mimic3/), some additional packages should be installed. Follow their [quick start guide](https://github.com/MycroftAI/mimic3/?tab=readme-ov-file#mycroft-tts-plugin).

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
   - [Coqui STT](https://github.com/coqui-ai/STT) (Formerly [Mozilla DeepSpeech](https://github.com/mozilla/DeepSpeech))
4. Large Language Models, based on:
   - [OpenAI GPT](https://openai.com/gpt-4)
5. Speech Synthesis / Text-to-Speech with:
   - [Piper](https://github.com/rhasspy/piper)

### Run Tests

A number of test scripts are available to verify the working of the individual components in the pipeline.  
Run a test by calling the test script from the main directory.

```bash
python tests/test_[something].py
```

## TODO

Keep track of the progress of this project below:

- [x] Wakeword Algorithm
- [x] Automatic Speech Recognition Model, integrate multiple models:
- [x] Speech to Text Model, Integrate multiple models:
- [ ] Speaker Identification Model
- [ ] LLM Integration
  - [x] OpenAI ChatGPT
  - [ ] Local Webserver model (TinyLLama / Gemma)
- [ ] LLM Tool Learning
- [ ] Tool Access Integration

## Similar Projects

This project is supposed to be a proof-of-concept.  
There are a lot of interesting projects out there that are developed to a more mature point.  
Go check them out!

- [Leon](https://github.com/leon-ai/leon)
- [Mycroft](https://github.com/MycroftAI/mycroft-core)
- [SpeechBrain](https://github.com/speechbrain/speechbrain)
- [rhasspy3](https://github.com/rhasspy/rhasspy3/)
- [and more...](https://github.com/topics/voice-assistants)
