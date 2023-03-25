from fastapi import FastAPI
from fastapi import File, UploadFile, HTTPException
# import zstandard as zstd
from pydantic import BaseModel

app = FastAPI()

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
    if audio_file.content_type not in ["audio/mp3", "audio/wave", "audio/flac"]:
        raise HTTPException(
            status_code=400, detail="Only MP3, WAV, and FLAC files are supported.")

    # Save the uploaded file
    with open(audio_file.filename, "wb") as output_file:
        output_file.write(audio_file.file.read())

    # Compress the uploaded file (optional)
    # compress_audio(audio_file.filename, f"{audio_file.filename}.compressed")

    return {"filename": audio_file.filename}

# Implement the basic health check service:


@app.get("/health")
def health_check():
    return {"status": "ok"}


