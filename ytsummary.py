import argparse
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from llama_cpp import Llama

parser = argparse.ArgumentParser(description='Summarise YouTube videos via the built in transcriptions')
parser.add_argument('id', help="Alphanumeric id of YouTube video, youtu.be/[id] or youtube.com/watch?v=[id]")
parser.add_argument('-s', '--stream', action='store_true', default=False, help="Output text as soon as it's created")
parser.add_argument('-d', '--detailed', action='store_true', default=False, help="Summarise every 5 minute chunk of the video")
parser.add_argument('-q', '--quick', action='store_true', default=False, help="Use smaller context LLM for faster inference")
parser.add_argument('-l', '--long_video', action='store_true', default=False, help="Use larger context LLM for longer videos, EXPERIMENTAL")
parser.add_argument('-o', '--out', action='store_true', default=False, help="Also output into .txt file, can be used with -t")
parser.add_argument('-t', '--transcript', action='store_true', default=False, help="Output full transcript only, no summarisation")
args = parser.parse_args()

def out(text):
    outfile = "output/" + video_id + ".txt"
    with open(outfile, "a") as f:
        f.write(text+"\n")

def sys_prompt():
    syspmt = ("### System: You are an AI assistant that summarises videos based on it's audio transcript. You only use "
              "information and context from the transcript, in other words, you do not state anything that is not "
              "explicitly stated in the transcript.\n\n")
    return syspmt

def quick_llm(text):
    path = "models/llongorca-7b-16k.ggmlv3.q4_K_M.bin"
    llama = Llama(model_path=path, n_gpu_layers=35, seed=-1, n_ctx=4096, rope_freq_scale=0.5)
    if args.detailed:
        for sections in text:
            section = ''.join(sections)
            output = llama(sys_prompt()+'### Instruction:\n\nList the details from the section of video shown here:\n"' +section +
                           '"\n\n### Response:\n', max_tokens=2048, temperature=0.5, stream=args.stream)
            display(output)
    else:
        output = llama(sys_prompt()+'### Instruction:\n\nSummarise the following concisely:\n"' + text + '"\n\n### Response:\n',
                     max_tokens=2048, stop=['###'], stream=args.stream, temperature=0.4)
        display(output)

def llm(text):
    path = "models/llongorca-7b-16k.ggmlv3.q4_K_M.bin"
    llama = Llama(model_path=path, n_gpu_layers=33, seed=-1, n_ctx=16384, rope_freq_scale=0.25)
    output = llama(sys_prompt()+'### Instruction:\n\nAccurately summarise all important information from the following and do not add extra information:\n"'
                   + text + '"\n\n### Response:\n', max_tokens=4096, stop=['###'], stream=args.stream, temperature=0.3, echo=True)
    display(output)

def display(output):
    if args.stream:
        for x in output:
            print(x['choices'][0]['text'], end="")
    else:
        print(output['choices'][0]['text'], end="")
        if args.out:
            out(output['choices'][0]['text'])

def get_transcript(id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(id)
    except TranscriptsDisabled:
        return None
    length = transcript[-1]['start'] + transcript[-1]['duration']
    n_segments = int(length / 60 / 5)
    segments = [[] for i in range(n_segments + 1)]
    for line in transcript:
        segments[int(line['start'] / 60 / 5)].append(line['text'] + " ")
    return segments

def combine_sub(segments):
    return ''.join([''.join(s) for s in segments])

def summary(segments):
    all_text = combine_sub(segments)
    if args.long_video:
        mid = len(segments)//2
        a = combine_sub(segments[:mid])
        b = combine_sub(segments[mid:])
        print("\n\nPart 1 of 2:\n\n")
        llm(a)
        print("\n\nPart 2 of 2:\n\n")
        llm(b)
    elif args.detailed:
        quick_llm(segments)
    else:
        all_text = combine_sub(segments)
        if args.quick:
            quick_llm(all_text)
        else:
            llm(all_text)


if __name__ == '__main__':
    video_id = args.id
    subs = get_transcript(video_id)
    if args.transcript:
        transcript = combine_sub(subs)
        print(transcript)
        if args.out:
            out(transcript)
    else:
        summary(subs)
