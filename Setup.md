# Setup Guide

In order to install the dependencies, initiate a conda environment from the `environment.yml` file.

```bash
conda env create -f environment.yml
```

If changes are made, the environment can be exported using the provided script.

```bash
bash export-environment.sh
```

## Large Language Model

Depending on the large language model provider you wish to use, additional setup steps are required.

### OpenAI

To use [OpenAI](https://openai.com/) GPT models as your LLM backend, you have to create a `.env` file with your [API key](https://platform.openai.com/api-keys).

```bash
OPENAI_API_KEY=YOUR-KEY
```

### LlamaEdge (self-hosted)

To use a self-hosted model, the [llamaedge](https://llamaedge.com/) framework is highly encouraged as it supports a number of pre-trained models as well as your own fine-tuned ones.

To get up and running with LLamaEdge, follow the instructions in their [quickstart guide](https://github.com/LlamaEdge/LlamaEdge#readme).

## Text To Speech Models

### Mimic3

To use [MycroftAI/mimic3](https://github.com/MycroftAI/mimic3/), some additional packages should be installed. Follow their [quick start guide](https://github.com/MycroftAI/mimic3/?tab=readme-ov-file#mycroft-tts-plugin).
