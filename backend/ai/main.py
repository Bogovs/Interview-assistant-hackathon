from dotenv import load_dotenv
from mutagen.mp3 import MP3
import tiktoken
import openai
import os


class User:
   def __init__(self) -> None:
      self.file_path: str = None
      self.prompt: str = None
      self.tokens_num: int = None
      self.audio_length: float = None
      self.transcription: str = None
      self.gpt_summary: str = None
      self.gpt_custom: str = None


def whisper(file) -> str:
   """Return transcription of interview. Accept audio file path."""

   with open(file, 'rb') as f:
      transcription = openai.Audio.transcribe('whisper-1', f)
      transcription = transcription['text']
      return transcription


def gpt_summary(transcription: str)  -> str:
  """Returns summary of interview"""

  response_summary = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[
          {'role': 'system', 'content': 'You are an interview assistant'},
          {'role': 'user', 'content': f'Summ up this inerview:\n\n{transcription}'},
      ]
  )
  return response_summary['choices'][0]['message']['content']


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
     custom_cost = num_tokens_from_string(custom, 'r50k_base') / 1000  * 0.002
   else:
     custom_cost = 0

   return transcript_cost + summary_cost + custom_cost + length_cost


def main():
   load_dotenv()
   OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
   openai.api_key = OPENAI_API_KEY
   
   user = User()

   user.prompt = None
   user.file_path = 'short.mp3'
   user.audio_length = audio_length(user.file_path)

   if user.audio_length < 25: #checking for whisper limit
      user.transcription = whisper(user.file_path)
      user.tokens_num = num_tokens_from_string(user.transcription, 'r50k_base')

      if user.tokens_num <= 3500: #checking for gpt limit
         user.gpt_summary = gpt_summary(user.transcription)
         if user.prompt != None:
            user.gpt_custom = gpt_custom(user.transcription, user.prompt)
      else:
         return print('Tokens limit reached')
   
   else:
      return print('Too long audio')
   
   estimated_cost = cost(user.tokens_num, user.gpt_summary, user.gpt_custom, user.audio_length)
   
   output = {'transcription': user.transcription,
             'summary': user.gpt_summary,
             'custom': user.gpt_custom,
             'cost': estimated_cost}
   
   return output


if __name__ == '__main__':
   try:
      output = main()
      print(output)
   except:
      print('Something went wrong')
