<div align="center">
   <img src="assets/logo.jpeg" alt="SOLA" width="320" height="320" >
   <h1 align="center">Smart Offline-first LLM Assistant</h1>
</div>

## ℹ️ About

**SOLA** is a Smart Offline-first LLM Assistant.  
By adopting an offline-first approach to data and model execution, privacy is guaranteed.  
Still, its integration with LLM AI models and access to external (online) tools make it smart.

The authors of the project are:

- [Flor Sanders (fps2116)](https://www.florsanders.be)
- [Charan Santhirasegaran (cs4347)](mailto:cs4347@columbia.edu)

More information on the project can be found in the [report](./report.pdf) and [slides](./slides.pdf) included in the repository.

## 🔥 Quick Start

Follow the [Setup Guide](./Setup.md) to install all requirements.
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

## 🔍 Testing

A number of test scripts are available to verify the working of the individual components in the pipeline.  
Run a test by calling the test script from the main directory.

```bash
python tests/test_[something].py
```

## ✅ Benchmarking

The performance of a tool-llm on various sample tasks can be evaluated using the `evaluate_toolllm.py` script.  
The results from our experiments can be found in the `logs` directory.

## 🏛️ Architecture

The pipeline that powers the voice assistant stands on the shoulders of giants:

1. CLI Tool built on [Typer](https://github.com/tiangolo/typer)
2. Wakeword Detection with [openWakeWord](https://github.com/dscripka/openWakeWord)
3. Automatic Speech Recognition / Speech-to-Text with:
   - [OpenAI Whisper](https://openai.com/research/whisper)
   - [Vosk](https://alphacephei.com/vosk/install)
   - [Coqui STT](https://stt.readthedocs.io/en/latest/) (Formerly [Mozilla DeepSpeech](https://github.com/mozilla/DeepSpeech))
4. Large Language Model (LLM) integration with:
   - [LlamaEdge](https://llamaedge.com/)
     - Use Llama 3 8B for the best experience.
     - A notebook for fine-tuning TinyLlama for tool usage is included in the `finetuning` directory. The fine-tuned weights can be downloaded from [Google Drive](https://drive.google.com/file/d/1yvO-ZFmFi-S1Yc3Gr8kn3cOtnlD_NJ2o/view).
   - [OpenAI GPT 3/4](https://openai.com/gpt-4)
5. Speech Synthesis / Text-to-Speech with:
   - [Piper](https://github.com/rhasspy/piper)
   - [Coqui TTS](https://docs.coqui.ai/en/dev/index.html) (Formerly [Mozilla TTS](https://github.com/mozilla/TTS))
   - [MycroftAI/mimic3](https://github.com/MycroftAI/mimic3)

## 🚀 Similar Projects

This project is supposed to be a proof-of-concept.  
There are a lot of interesting projects out there that are developed to a more mature point.  
Go check them out!

- [Leon](https://github.com/leon-ai/leon)
- [Mycroft](https://github.com/MycroftAI/mycroft-core)
- [SpeechBrain](https://github.com/speechbrain/speechbrain)
- [rhasspy3](https://github.com/rhasspy/rhasspy3/)
- [and more...](https://github.com/topics/voice-assistants)
