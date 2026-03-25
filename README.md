# Voice_agent

Voice_agent is a multi-part project demonstrating a conversational assistant. It includes:

- a Python backend with optional CLI voice assistant (microphone + offline TTS), persistent history, intent tools and web search
- a FastAPI backend used by a React (Vite) frontend for a polished web chat UI

This repo contains both backend and frontend code so you can run either the full local voice assistant (CLI) or the web chat UI.

---

## Highlights (changes in this workspace)

- Web frontend (Vite + React) with a professional, ChatGPT-like dark UI (avatars, typing indicator, timestamps, animated messages).
- Frontend accepts voice input (speech-to-text) from the user — assistant replies are text-only in the web UI.
- FastAPI endpoint at `POST /chat` that the frontend calls to get assistant responses.

---

## Quick start — Frontend + Backend (recommended)

1) Start the backend API (FastAPI). From project root:

```bash
pip install -r requirements.txt
# run backend API for the frontend
uvicorn backend.api:app --reload --port 8000
```

2) Start the frontend (from `frontend/`):

```bash
cd frontend
npm install   # only if dependencies are missing
npm run dev
```

Open the dev server URL (usually `http://localhost:5173`) — the frontend will call the backend at `http://localhost:8000/chat`.

---

## Run the original CLI voice assistant (optional)

The repository also includes a CLI-style voice assistant using `main.py`. This version listens from your microphone and uses local/offline TTS (`pyttsx3`) by default:

```bash
# activate virtualenv first
python backend/main.py
```

Note: the CLI assistant and the FastAPI/web frontend are separate entry points.

---

## Environment variables

Create a `.env` file in the repo root with the keys used by the backend (Azure, Mongo, Tavily, etc.):

```
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
AZURE_OPENAI_API_VERSION=2023-10-01
AZURE_DEPLOYMENT=your_deployment_name

MONGO_URI=your_mongodb_connection_string

TAVILY_API_KEY=your_tavily_api_key
```

Adjust values to your environment. The FastAPI backend reads the same configuration when running `uvicorn backend.api:app`.

---

## Notes & UX decisions

- The web UI intentionally keeps assistant replies as text (no TTS) while allowing users to speak to submit queries. This provides a clean, readable conversation flow and avoids overlapping speech playback in the browser.
- The frontend shows a typing placeholder while the backend is processing; messages are animated and timestamped for a realistic chat feel.
- CORS is enabled on the backend to allow the frontend to talk to `http://localhost:8000` during development.

---

## Troubleshooting

- If the frontend cannot reach the backend, confirm the backend is running on port `8000` and no firewall blocks it.
- If microphone access is blocked, allow the page to use your microphone in the browser prompt.
- For PyAudio install issues on Windows, try `pip install pipwin` then `pipwin install pyaudio`.

---

## Contributing

Feel free to open issues or pull requests. If you want help wiring TTS back into the frontend (client-side audio playback), I can add an option to play assistant responses via `SpeechSynthesis` or a backend-generated audio stream.

---

## Author

Harsh Jaiswal
