# from dotenv import load_dotenv
from mutagen.mp3 import MP3
import tiktoken
import openai
import os
import re
from pyannote.audio import Pipeline
from pydub import AudioSegment
from subprocess import run
import whisper
import webvtt


class User:
    def __init__(self) -> None:
        self.file_path: str = None
        self.prompt: str = None
        self.tokens_num: int = None
        self.audio_length: float = None
        self.transcription: str = None
        self.gpt_summary: str = None
        self.gpt_custom: str = None


def whisper_transcribe(audio_file) -> str:
    """Return transcription of interview. Accept audio file path."""

    # with open(audio_file, 'rb') as f:
    #     transcription = openai.Audio.transcribe('whisper-1', f)
    #     transcription = transcription['text']
    #     return transcription

    model = whisper.load_model("base")
    result = model.transcribe(audio_file)
    return result["text"]


def millisec(timeStr):
    spl = timeStr.split(":")
    s = (int)((int(spl[0]) * 60 * 60 +
               int(spl[1]) * 60 + float(spl[2])) * 1000)
    return s


def cleanup(file_name: str):
    ''' Delete all the temporary files '''
    to_remove = [".json", ".srt", ".tsv", ".txt", ".vtt", ".wav"]
    for i in range(len(to_remove) - 1):
        os.remove(f"{file_name}{to_remove[i]}")


def diarization(audio_file_path: str, file_name: str) -> dict:
    print("file_name:", file_name)
    # 1
    t1 = 0 * 1000  # Works in milliseconds
    t2 = 20 * 60 * 1000

    newAudio = AudioSegment.from_wav(audio_file_path)
    new_audio_file = f"{file_name}.wav"
    print("new_audio_file:", new_audio_file)
    a = newAudio[t1:t2]
    a.export(new_audio_file, format="wav")

    # 2
    audio = AudioSegment.from_wav(new_audio_file)
    spacermilli = 2000
    spacer = AudioSegment.silent(duration=spacermilli)
    audio = spacer.append(audio, crossfade=0)
    new_audio_file_2 = f"{file_name}2.wav"
    print("new_audio_file_2:", new_audio_file_2)
    audio.export(new_audio_file_2, format='wav')

    # 3
    pipeline = Pipeline.from_pretrained(
        'pyannote/speaker-diarization', use_auth_token="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")  # Temporary Hard Coded Token
    path = {'uri': 'backend', 'audio': new_audio_file_2}
    pipe = pipeline(path)

    with open(f"{file_name}.txt", "w") as text_file:
        text_file.write(str(pipe))

    print(*list(pipe.itertracks(yield_label=True))[:10], sep="\n")

    # 4
    dz = open(f"{file_name}.txt").read().splitlines()
    dzList = []
    for l in dz:
        start, end = tuple(re.findall(
            '[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=l))
        start = millisec(start) - 2000
        end = millisec(end) - 2000
        lex = not re.findall('SPEAKER_01', string=l)
        dzList.append([start, end, lex])

    print(*dzList[:10], sep='\n')

    # 5
    sounds = spacer
    segments = []

    dz = open(f"{file_name}.txt").read().splitlines()
    for l in dz:
        start, end = tuple(re.findall(
            '[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=l))
        start = int(millisec(start))  # milliseconds
        end = int(millisec(end))  # milliseconds

        segments.append(len(sounds))
        sounds = sounds.append(audio[start:end], crossfade=0)
        sounds = sounds.append(spacer, crossfade=0)

    # Exports to a wav file in the current path.
    post_processing_file = f"{file_name}new.wav"
    sounds.export(post_processing_file, format="wav")

    print("segments:", segments[:8])
    print("post_processed_saved_file_name:", post_processing_file)

    del sounds, pipeline, spacer, audio, dz

    # 6
    command = f"whisper {post_processing_file} --language en --model base"
    run(command, shell=True)
    print("whisper model ran via command line")

    # 7
    post_processing_file_name = post_processing_file.split(".")[0]
    captions = [[(int)(millisec(caption.start)), (int)(millisec(
        caption.end)),  caption.text] for caption in webvtt.read(f"{post_processing_file_name}.vtt")]
    print(*captions[:8], sep='\n')

    # 8
    preS = '<!DOCTYPE html>\n<html lang="en">\n  <head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <meta http-equiv="X-UA-Compatible" content="ie=edge">\n    <title>Interview</title>\n    <style>\n        body {\n            font-family: sans-serif;\n            font-size: 18px;\n            color: #111;\n            padding: 0 0 1em 0;\n        }\n        .l {\n          color: #050;\n        }\n        .s {\n            display: inline-block;\n        }\n        .e {\n            display: inline-block;\n        }\n        .t {\n            display: inline-block;\n        }\n        #player {\n\t\tposition: sticky;\n\t\ttop: 20px;\n\t\tfloat: right;\n\t}\n    </style>\n  </head>\n  <body>\n    <h2> Interview Transcription </h2>\n  <div  id="player"></div>\n    <script>\n      var tag = document.createElement(\'script\');\n      tag.src = "https://www.youtube.com/iframe_api";\n      var firstScriptTag = document.getElementsByTagName(\'script\')[0];\n      firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);\n      var player;\n      function onYouTubeIframeAPIReady() {\n        player = new YT.Player(\'player\', {\n          height: \'210\',\n          width: \'340\',\n          videoId: \'SGzMElJ11Cc\',\n        });\n      }\n      function setCurrentTime(timepoint) {\n        player.seekTo(timepoint);\n   player.playVideo();\n   }\n    </script><br>\n'
    postS = '\t</body>\n</html>'

    html = list(preS)

    for i in range(len(segments)):
        idx = 0
        for idx in range(len(captions)):
            if captions[idx][0] >= (segments[i] - spacermilli):
                break

        while (idx < (len(captions))) and ((i == len(segments) - 1) or (captions[idx][1] < segments[i+1])):
            c = captions[idx]

            start = dzList[i][0] + (c[0] - segments[i])

            if start < 0:
                start = 0
            idx += 1

            start = start / 1000.0
            startStr = '{0:02d}:{1:02d}:{2:02.2f}'.format((int)(start // 3600),
                                                          (int)(start %
                                                                3600 // 60),
                                                          start % 60)

            html.append('\t\t\t<div class="c">\n')
            html.append(
                f'\t\t\t\t<a class="l" href="#{startStr}" id="{startStr}">link</a> |\n')
            html.append(
                f'\t\t\t\t<div class="s"><a href="javascript:void(0);" onclick=setCurrentTime({int(start)})>{startStr}</a></div>\n')
            html.append(
                f'\t\t\t\t<div class="t">{"[---]" if dzList[i][2] else "[-]"} {c[2]}</div>\n')
            html.append('\t\t\t</div>\n\n')

    html.append(postS)
    html_str = "".join(html)

    with open(f"{post_processing_file_name}.html", "w") as html_file:
        html_file.write(html_str)

    with open(f"{post_processing_file_name}.txt", "r") as text_file:
        transcription = text_file.read()

    cleanup(file_name=post_processing_file_name)

    return {
        "html": html_str,
        "transcription": transcription
    }


def transcribe_and_summarize(audio_file: str) -> dict:
    ''' Return Transcription and Summarization '''

    # with open(audio_file, 'rb') as audio:
    #     transcription = openai.Audio.transcribe('whisper-1', audio)
    #     transcription = transcription['text']

    data = diarization(audio_file_path=audio_file,
                       file_name=audio_file.split(".")[0])

    response_summary = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'system', 'content': 'You are an interview assistant'},
            {'role': 'user',
                'content': f'Summ up this inerview:\n\n{data["transcription"]}'},
        ]
    )
    return {
        "html": data["html"],
        "transcription": data["transcription"],
        "summary": response_summary['choices'][0]['message']['content']
    }


# def gpt_summary(transcription: str) -> str:
#     """Returns summary of interview"""

#     response_summary = openai.ChatCompletion.create(
#         model='gpt-3.5-turbo',
#         messages=[
#             {'role': 'system', 'content': 'You are an interview assistant'},
#             {'role': 'user', 'content': f'Summ up this inerview:\n\n{transcription}'},
#         ]
#     )
#     return response_summary['choices'][0]['message']['content']


def gpt_custom(transcription: str, custom_prompt: str) -> str:
    """Returns custom prompt output"""

    response_custom = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'system', 'content': 'You are an interview assistant'},
            {'role': 'user', 'content': f'{custom_prompt}\n\n{transcription}'},
        ]
    )
    return response_custom['choices'][0]['message']['content']


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a subtitles"""

    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def audio_length(file) -> float:
    """Returns the length of audio file"""

    audio = MP3(file)
    return audio.info.length / 60


def cost(tokens_num: int, summary: str, custom: str, length: float) -> float:
    transcript_cost = tokens_num * 0.002
    summary_cost = num_tokens_from_string(summary, 'r50k_base') / 1000 * 0.002
    length_cost = length * 0.006

    if custom != None:
        custom_cost = num_tokens_from_string(
            custom, 'r50k_base') / 1000 * 0.002
    else:
        custom_cost = 0

    return transcript_cost + summary_cost + custom_cost + length_cost


# def main():
#     # load_dotenv()
#     OPENAI_API_KEY = "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"
#     openai.api_key = OPENAI_API_KEY

#     user = User()

#     user.prompt = None
#     user.file_path = 'short.mp3'
#     user.audio_length = audio_length(user.file_path)

    # if user.audio_length < 25:  # checking for whisper limit
    #     user.transcription = whisper(user.file_path)
    #     user.tokens_num = num_tokens_from_string(
    #         user.transcription, 'r50k_base')

    #     if user.tokens_num <= 3500:  # checking for gpt limit
    #         user.gpt_summary = gpt_summary(user.transcription)
    #         if user.prompt != None:
    #             user.gpt_custom = gpt_custom(user.transcription, user.prompt)
    #     else:
    #         return print('Tokens limit reached')

    # else:
    #     return print('Too long audio')

    # estimated_cost = cost(user.tokens_num, user.gpt_summary,
    #                       user.gpt_custom, user.audio_length)

    # output = {'transcription': user.transcription,
    #           'summary': user.gpt_summary,
    #           'custom': user.gpt_custom,
    #           'cost': estimated_cost}

    # return output


# if __name__ == '__main__':
#     try:
#         # output = main()
#         # print(output)
#     except:
#         print('Something went wrong')
