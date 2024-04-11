# Setup Guide for `llama.cpp` on Nvidia Jetson Nano 2GB

This is a full account of the steps I ran to get `llama.cpp` running on the Nvidia Jetson Nano 2GB. It accumulates multiple different fixes and tutorials, whose contributions are referenced at the bottom of this README.

## Procedure

At a high level, the procedure to install `llama.cpp` on a Jetson Nano consists of 3 steps.

1. Compile the `gcc 8.5` compiler from source.

2. Compile `llama.cpp` from source using the `gcc 8.5` compiler.

3. Download a model.

4. Perform inference.

As step 1 and 2 take a long time, I have uploaded the resulting [binaries for download](https://github.com/FlorSanders/Smart_Offline_LLM_Assistant/raw/jetson-nano/models/llm/llama_binaries.zip) in the repository. Simply download, unzip and follow step 3 and 4 to perform inference.

### GCC Compilation

1. Compile the GCC 8.5 compiler from source on the Jetson nano.  
   **NOTE:** The `make -j6` command takes a long time. I recommend running it overnight in a `tmux` session. Additionally, it requires quite a bit of disk space so make sure to leave at least 8GB of free space on the device before starting.

```bash
wget https://bigsearcher.com/mirrors/gcc/releases/gcc-8.5.0/gcc-8.5.0.tar.gz
sudo tar -zvxf gcc-8.5.0.tar.gz --directory=/usr/local/
cd /usr/local/
./contrib/download_prerequisites
mkdir build
cd build
sudo ../configure -enable-checking=release -enable-languages=c,c++
make -j6
make install
```

2. Once the `make install` command ran successfully, you can clean up disk space by removing the `build` directory.

```bash
cd /usr/local/
rm -rf build
```

3. Set the newly installed GCC and G++ in the environment variables.

```bash
export CC=/usr/local/bin/gcc
export CXX=/usr/local/bin/g++
```

4. Double check whether the install was indeed successful (both commands should say `8.5.0`).

```bash
gcc --version
g++ --version
```

### `llama.cpp` Compilation

5. Start by cloning the repository and rolling back to a known working commit.

```bash
git clone git@github.com:ggerganov/llama.cpp.git
git checkout a33e6a0
```

6. Edit the Makefile and apply the following changes  
   (save to `file.patch` and apply with `git apply --stat file.patch`)

```bash
diff --git a/Makefile b/Makefile
index 068f6ed0..a4ed3c95 100644
--- a/Makefile
+++ b/Makefile
@@ -106,11 +106,11 @@ MK_NVCCFLAGS = -std=c++11
 ifdef LLAMA_FAST
 MK_CFLAGS     += -Ofast
 HOST_CXXFLAGS += -Ofast
-MK_NVCCFLAGS  += -O3
+MK_NVCCFLAGS += -maxrregcount=80
 else
 MK_CFLAGS     += -O3
 MK_CXXFLAGS   += -O3
-MK_NVCCFLAGS  += -O3
+MK_NVCCFLAGS += -maxrregcount=80
 endif

 ifndef LLAMA_NO_CCACHE
@@ -299,7 +299,6 @@ ifneq ($(filter aarch64%,$(UNAME_M)),)
 	# Raspberry Pi 3, 4, Zero 2 (64-bit)
 	# Nvidia Jetson
 	MK_CFLAGS   += -mcpu=native
-	MK_CXXFLAGS += -mcpu=native
 	JETSON_RELEASE_INFO = $(shell jetson_release)
 	ifdef JETSON_RELEASE_INFO
 		ifneq ($(filter TX2%,$(JETSON_RELEASE_INFO)),)
```

- **NOTE:** If you rather make the changes manually, do the following:

  - Change `MK_NVCCFLAGS += -O3` to `MK_NVCCFLAGS += -maxrregcount=80` on line 109 and line 113.

  - Remove `MK_CXXFLAGS += -mcpu=native` on line 302.

6. Build the `llama.cpp` source code.

```bash
make LLAMA_CUBLAS=1 CUDA_DOCKER_ARCH=sm_62 -j 6
```

### Download a model

7. Download a model to the device

```bash
wget https://huggingface.co/second-state/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/TinyLlama-1.1B-Chat-v1.0-Q5_K_M.gguf
```

- **NOTE**: Due to the limited memory of the Nvidia Jetson Nano 2GB, I have only been able to successfully run the [second-state/TinyLlama-1.1B-Chat-v1.0-GGUF](https://huggingface.co/second-state/TinyLlama-1.1B-Chat-v1.0-GGUF) on the device.  
  Attempts were made to get [second-state/Gemma-2b-it-GGUF](https://huggingface.co/second-state/Gemma-2b-it-GGUF) working, but these did not succeed.

### Perform inference

8. Test the main inference script

```bash
./main -m ./TinyLlama-1.1B-Chat-v1.0-Q5_K_M.gguf -ngl 33  -c 2048 -b 512 -n 128 --keep 48
```

9. Run the live server

```bash
./server -m ./TinyLlama-1.1B-Chat-v1.0-Q5_K_M.gguf -ngl 33  -c 2048 -b 512 -n 128
```

10. Test the web server functionality using curl

```bash
curl --request POST \
    --url http://localhost:8080/completion \
    --header "Content-Type: application/json" \
    --data '{"prompt": "Building a website can be done in 10 simple steps:","n_predict": 128}'
```

You can now run a large language model on this tiny and cheap edge device.
Have fun!

## References

- [@otaGran TX2 Guide](https://github.com/ggerganov/llama.cpp/issues/4123#issuecomment-1965272660)
- [@FantasyGmm Guide](https://github.com/ggerganov/llama.cpp/issues/4123#issuecomment-1878026179)
- [@rvandernoot Guide](https://github.com/ggerganov/llama.cpp/issues/4099#issuecomment-1887338898)
- [`llama.cpp` server documentation](https://github.com/ggerganov/llama.cpp/tree/master/examples/server)
