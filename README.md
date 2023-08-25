# YTSummarise

Summarise YouTube videos via transcripts and Llama2 LLM.

Optimised for 8GB VRAM.

Colab notebook version: https://colab.research.google.com/github/addis0nl/YTSummarise/blob/main/YTSummarise.ipynb

## Installation:

```shell
pip install youtube_transcript_api
$env:FORCE_CMAKE=1
$env:CMAKE_ARGS="-DLLAMA_CUBLAS=on"
pip install llama-cpp-python
```
Extract this repository.

Download https://huggingface.co/TheBloke/LlongOrca-7B-16K-GGML/resolve/main/llongorca-7b-16k.ggmlv3.q4_K_M.bin and place into models folder.

## To use:

`python3 ytsummary.py [video id]`

>-h for more options
