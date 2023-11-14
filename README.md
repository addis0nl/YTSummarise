# YTSummarise

Summarise YouTube videos via transcripts and Llama2 LLM.

Optimised for 8GB VRAM.

#### Colab notebook version: 

https://colab.research.google.com/drive/1DKMs2d2gUVuFInYDL15QTEnHvY8ulnSc?usp=sharing

## Installation:

```shell
pip install youtube_transcript_api
$env:FORCE_CMAKE=1
$env:CMAKE_ARGS="-DLLAMA_CUBLAS=on"
pip install llama-cpp-python==0.1.78
```
Extract this repository.

Download https://huggingface.co/TheBloke/LlongOrca-7B-16K-GGML/resolve/main/llongorca-7b-16k.ggmlv3.q4_K_M.bin and place into *models* folder (create one).

## To use:

```
python3 ytsummary.py [video id]
```

`-h` or `--help` for more options
