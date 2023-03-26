from fastapi import FastAPI
from fastapi import File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run
# import zstandard as zstd

from dotenv import load_dotenv
import openai
from os import getenv, getcwd
from pydantic import BaseModel
from predict import diarization, transcribe_and_summarize, gpt_custom

allowed_origins = [
    "*"  # Temporary value set to *
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["POST"]
)

# Implement the audio file compression logic (optional):
# def compress_audio(input_file_path, output_file_path):
#     cctx = zstd.ZstdCompressor(level=3)
#     with open(input_file_path, "rb") as input_file, open(output_file_path, "wb") as output_file:
#         compressed_data = cctx.compress(input_file.read())
#         output_file.write(compressed_data)

# Implement the custom prompt endpoint:


class QA(BaseModel):
    ''' Static Typing for Parameters '''
    transcription: str
    question: str


@app.post("/custom-prompt")
def custom_prompt(params: QA):
    ''' QA Endpoint '''
    qa_prompt = gpt_custom(
        transcription=params.transcription, question=params.question)
    return {"answer": qa_prompt}


@app.post("/audio")
def upload_audio_file(audio_file: UploadFile = File(...)):
    '''Audio Upload and Processing  '''
    # Check if the uploaded file is an audio file
    if audio_file.content_type not in ["audio/mp3", "audio/wave", "audio/wav", "audio/x-wav"]:
        raise HTTPException(
            status_code=400, detail="Only MP3 and WAV files are supported.")

    # Save the uploaded file
    with open(audio_file.filename, "wb") as output_file:
        output_file.write(audio_file.file.read())

    # Compress the uploaded file (optional)
    # compress_audio(audio_file.filename, f"{audio_file.filename}.compressed")

    processed = transcribe_and_summarize(audio_file=audio_file.filename)
    return {"output": processed}


@app.get("/health")
def health_check():
    ''' Health Check '''
    return {"status": "ok"}


@app.post("/test")
def test():
    ''' Test Endpoint '''
    diarized = diarization(audio_file_path="./short.wav", file_name="xyz")
    return {"output": diarized}


# Run the server:
if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8000)
