from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import edge_tts
import io

app = FastAPI()

class TTSRequest(BaseModel):
    text: str
    voice: str = "en-US-GuyNeural"

@app.get("/")
def root():
    return {"status": "Edge TTS API is running"}

@app.post("/tts")
async def text_to_speech(request: TTSRequest):
    try:
        communicate = edge_tts.Communicate(request.text, request.voice)
        audio_buffer = io.BytesIO()

        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_buffer.write(chunk["data"])

        audio_buffer.seek(0)

        return StreamingResponse(
            audio_buffer,
            media_type="audio/mpeg",
            headers={"Content-Disposition": "attachment; filename=audio.mp3"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
