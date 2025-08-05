from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from gtts import gTTS
import uuid
import os

app = FastAPI()

AUDIO_FOLDER = "audio"
os.makedirs(AUDIO_FOLDER, exist_ok=True)

app.mount("/audio", StaticFiles(directory=AUDIO_FOLDER), name="audio")
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def get_ui(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/speak")
async def speak(request: Request):
    try:
        data = await request.json()
        text = data.get("text")

        if not text:
            return JSONResponse(status_code=400, content={"error": "Text not provided"})

        filename = f"{uuid.uuid4().hex}.mp3"
        filepath = os.path.join(AUDIO_FOLDER, filename)

        tts = gTTS(text)
        tts.save(filepath)

        return FileResponse(filepath, media_type="audio/mpeg", filename=filename)

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
