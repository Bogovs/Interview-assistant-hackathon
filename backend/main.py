from fastapi import FastAPI
from fastapi import File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run
# import zstandard as zstd

from dotenv import load_dotenv
import openai
from os import getenv, getcwd
from pydantic import BaseModel
from predict import User, diarization, transcribe_and_summarize

allowed_origins = [
    "http://localhost:5173"
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
    question: str
    answer: str


@app.post("/custom_prompt")
def custom_prompt(params: QA):
    # Process the question and answer and return the result
    result = f"question is {params.question} and answer is {params.answer}"
    return {"result": result}


# Implement the audio file endpoint:
@app.post("/audio")
def upload_audio_file(audio_file: UploadFile = File(...)):
    # Check if the uploaded file is an audio file
    if audio_file.content_type not in ["audio/mp3", "audio/wave", "audio/wav"]:
        raise HTTPException(
            status_code=400, detail="Only MP3 and WAV files are supported.")

    # Save the uploaded file
    with open(audio_file.filename, "wb") as output_file:
        output_file.write(audio_file.file.read())

    # Compress the uploaded file (optional)
    # compress_audio(audio_file.filename, f"{audio_file.filename}.compressed")

    processed = transcribe_and_summarize(audio_file=audio_file.filename)
    return {"output": processed}

# Implement the basic health check service:


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/test")
def test():
    diarization(audio_file_path="./short.wav", file_name="xyz")
    return {"status": "ran!"}


# Run the server:
if __name__ == "__main__":
    load_dotenv()
    OPENAI_API_KEY = getenv("OPENAI_API_KEY")
    openai.api_key = OPENAI_API_KEY

    user = User()
    run(app, host="0.0.0.0", port=8000)
