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

## TODO

This repository is a work in progress, some things that remain to be done are:

- [ ] Automatic Speech Recognition Model
- [ ] Speech to Text Model
- [ ] Speaker Identification Model
- [ ] LLM Integration
- [ ] LLM Tool Learning
- [ ] Tool Access Integration
