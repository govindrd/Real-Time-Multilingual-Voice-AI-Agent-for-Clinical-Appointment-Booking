# backend/asr.py

import os
import logging
import tempfile
import httpx

logger = logging.getLogger(__name__)

OPENAI_KEY = os.getenv("OPENAI_API_KEY")


# -------------------------
# MAIN TRANSCRIBE FUNCTION
# -------------------------
async def transcribe_audio_bytes(audio_bytes: bytes, lang: str = "en") -> str:
    """
    Transcribe audio using:
    1. OpenAI Whisper API (if key present)
    2. Local fallback
    """

    if OPENAI_KEY:
        try:
            return await _transcribe_openai(audio_bytes)
        except Exception as e:
            logger.error(f"OpenAI ASR failed: {e}")

    # fallback
    return _local_fallback(audio_bytes)


# -------------------------
# OPENAI WHISPER API
# -------------------------
async def _transcribe_openai(audio_bytes: bytes) -> str:
    url = "https://api.openai.com/v1/audio/transcriptions"

    headers = {
        "Authorization": f"Bearer {OPENAI_KEY}"
    }

    # Save temp file (OpenAI needs file upload)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        f.write(audio_bytes)
        temp_path = f.name

    files = {
        "file": open(temp_path, "rb"),
        "model": (None, "whisper-1")
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(url, headers=headers, files=files)

    if response.status_code != 200:
        raise Exception(f"ASR failed: {response.text}")

    result = response.json()

    return result.get("text", "")


# -------------------------
# LOCAL FALLBACK
# -------------------------
def _local_fallback(audio_bytes: bytes) -> str:
    logger.info("Using fallback ASR (mock)")
    return "[fallback transcript]"