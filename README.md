# Multimodal Chat Backend

FastAPI backend that forwards text + image messages to your model at
`https://api.experientiallabs.ai/v1` and returns the reply as JSON.

## Endpoints

- `GET /` — a simple browser test page (upload an image + type a message).
- `POST /chat` — multipart form with fields:
  - `message` (text, required)
  - `image` (file, optional)
  - returns `{"response": "..."}` or `{"error": "..."}`
- `GET /health` — returns `{"status": "ok", "model": "<MODEL_NAME>"}`

## Before deploying

1. Open `main.py` and set `MODEL_NAME` to the real model id from your
   provider (currently set to the placeholder `"gpt-4o-mini"` for testing).
2. Make sure `API_KEY` is your real key (don't commit it to a public repo —
   see "Securing the key" below).

## Deploy to Railway (recommended, easiest)

1. Push this `backend/` folder to a GitHub repo (or just this folder as its
   own repo).
2. Go to https://railway.app → New Project → Deploy from GitHub repo.
3. Railway auto-detects the `Dockerfile` and builds/runs it.
4. Once deployed, Railway gives you a public URL like
   `https://yourapp.up.railway.app`. That's the `BASE_URL` you'll put into
   the Android app.
5. Test it: open `https://yourapp.up.railway.app/health` in a browser — you
   should see `{"status":"ok","model":"gpt-4o-mini"}`.

## Deploy to Render (alternative)

1. Push to GitHub.
2. Render dashboard → New → Web Service → connect the repo.
3. Render also auto-detects the `Dockerfile`. Set the instance type to Free
   or Starter.
4. You'll get a URL like `https://yourapp.onrender.com`.

## Run locally (for testing before you deploy)

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

Then open `http://localhost:8000` in a browser to use the test page, or
`http://<your-computer's-LAN-IP>:8000` from a phone on the same WiFi.

## Securing the API key (do this before going live)

Right now the key is hardcoded in `main.py`. Once you're ready to publish
the Android app, move it to an environment variable instead:

```python
import os
API_KEY = os.environ["EXPERIENTIAL_API_KEY"]
```

Then set `EXPERIENTIAL_API_KEY` in Railway/Render's environment variables
dashboard instead of committing it to code.
