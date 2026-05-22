Backend: FastAPI realtime agent

Run (dev):

1. Create a virtualenv and install requirements:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

2. Start the server:

```bash
uvicorn app:app --reload --port 8000
```

Notes
- The realtime WebSocket endpoint `/ws/audio` accepts JSON control messages for demo. See `app.py`.
- Configure environment variables in `.env` (OPENAI_API_KEY, REDIS_URL)
