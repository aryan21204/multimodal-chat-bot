import base64
from typing import Optional

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from openai import OpenAI

app = FastAPI()

# -----------------------------
# CORS (safe to leave open; a native Android app doesn't send an
# Origin header, and this also lets you test from a browser)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Model configuration
# -----------------------------

BASE_URL = "https://api.experientiallabs.ai/v1"
API_KEY = "*****************"

client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY,
    timeout=1200.0,
)

# TODO: replace with the real model id from your provider once you have it.
# This is just a placeholder so the app can be tested end-to-end.
MODEL_NAME = "gpt-4o-mini"


# -----------------------------
# Serve a simple test page (optional, handy for quick browser testing)
# -----------------------------
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def home():
    return FileResponse("static/index.html")


# -----------------------------
# Chat API (multimodal: text + optional image)
# -----------------------------

def encode_image_to_data_url(raw_bytes: bytes, content_type: str) -> str:
    b64 = base64.b64encode(raw_bytes).decode("utf-8")
    return f"data:{content_type};base64,{b64}"


@app.post("/chat")
async def chat(
    message: str = Form(...),
    image: Optional[UploadFile] = File(None),
):
    try:
        content = [{"type": "text", "text": message}]

        if image is not None:
            raw_bytes = await image.read()
            content_type = image.content_type or "image/jpeg"
            data_url = encode_image_to_data_url(raw_bytes, content_type)
            content.append(
                {
                    "type": "image_url",
                    "image_url": {"url": data_url},
                }
            )

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": content,
                }
            ],
            max_tokens=1500,
        )

        answer = response.choices[0].message.content

        return {"response": answer}

    except Exception as e:
        return {"error": str(e)}


@app.get("/health")
async def health():
    return {"status": "ok", "model": MODEL_NAME}
