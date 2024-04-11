# Setup Guide

Unfortunately, installing dependencies on the Jetson Nano is not as easy.  
The cause of this is mostly due the lack of support for Python versions >= 3.6.  
Below, we provide instructions to succesfully install the dependencies with Python 3.7.  
Unfortunately (again), as we are not using Python 3.6 the Cuda capabilities of the Jetson Nano will not be used.

Without further ado, here are the installation steps:

1. Perform a clean install on the Jetson Nano following [official instructions](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit#setup)
2. Run the following commands to install all the dependencies.
   - NOTE: For specific package versions, please refer to the [`requirements.txt`](./requirements.txt) file included in the repository.

```bash
# Update package registry
sudo apt update

# Install more recent versions of gcc (needed for succesful vosk install)
sudo add-apt-repository ppa:ubuntu-toolchain-r/test
sudo apt update
sudo apt install gcc-9
sudo apt install libstdc++6

# Install apt packages
sudo apt install portaudio19-dev
sudo apt-get install libespeak-ng1

# Install python & pip
sudo apt install python3.7
sudo apt install python3-pip
sudo apt-get install python3.7-dev
python3.7 -m pip install --upgrade pip

# Install dependencies
python3.7 -m pip install typer
python3.7 -m pip install openwakeword
python3.7 -m pip install pyaudio
python3.7 -m pip install vosk
wget https://github.com/coqui-ai/STT/releases/download/v1.4.0/stt-1.4.0-cp37-cp37m-linux_aarch64.whl
python3.7 -m pip install stt-1.4.0-cp37-cp37m-linux_aarch64.whl
python3.7 -m pip install --upgrade scikit-learn
python3.7 -m pip install --upgrade numpy
python3.7 -m pip install --upgrade scipy
python3.7 -m pip install --upgrade pandas
python3.7 -m pip install --upgrade matplotlib
python3.7 -m pip install openai
python3.7 -m pip install python-dotenv
python3.7 -m pip install tts
python3.7 -m pip uninstall torch torchaudio torchvision
python3.7 -m pip install torch torchaudio torchvision
python3.7 -m pip install mycroft-plugin-tts-mimic3[all]
python3.7 -m pip install langchain
```

Once installed, run the program using the following command

```
LD_PRELOAD=~/.local/lib/python3.7/site-packages/scikit_learn.libs/libgomp-d22c30c5.so.1.0.0:/usr/lib/aarch64-linux-gnu/libgomp.so.1 python3.7
```

## Large Language Model

Depending on the large language model provider you wish to use, additional setup steps are required.

### OpenAI

To use [OpenAI](https://openai.com/) GPT models as your LLM backend, you have to create a `.env` file with your [API key](https://platform.openai.com/api-keys).

```bash
OPENAI_API_KEY=YOUR-KEY
```

### LlamaEdge $\rightarrow$ Llama.cpp (self-hosted)

While [llamaedge](https://llamaedge.com/) is the easiest way to deploy LLMs on many devices, it was found not to be supported on the Nvidia Jetson Nano.

Instead use our [`llama.cpp`](./SetupJetsonNanoLLM.md) setup guide to deploy TinyLlama on the Nvidia Jetson.
