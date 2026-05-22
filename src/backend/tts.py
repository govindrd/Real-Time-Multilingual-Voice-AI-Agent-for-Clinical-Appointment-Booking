# backend/tts.py

import logging
from gtts import gTTS
from io import BytesIO

logger = logging.getLogger(__name__)


# -------------------------
# LANGUAGE MAP
# -------------------------
LANG_MAP = {
    "en": "en",
    "hi": "hi",
    "ta": "ta"
}


# -------------------------
# MAIN FUNCTION
# -------------------------
def synthesize_text_to_mp3_bytes(text: str, lang: str = "en") -> bytes:
    """
    Generate speech audio from text.
    Fallback TTS using gTTS.
    """

    lang_code = LANG_MAP.get(lang, "en")

    try:
        tts = gTTS(text=text, lang=lang_code)

        buf = BytesIO()
        tts.write_to_fp(buf)

        logger.info(f"TTS generated ({lang_code})")

        return buf.getvalue()

    except Exception as e:
        logger.exception("TTS failed: %s", e)
        return b""


# -------------------------
# OPTIONAL: CHUNKED TTS (SIMULATED STREAMING)
# -------------------------
def synthesize_stream(text: str, lang: str = "en"):
    """
    Simulate streaming by splitting text.
    (Real streaming requires cloud TTS)
    """
    sentences = text.split(". ")

    for sentence in sentences:
        yield synthesize_text_to_mp3_bytes(sentence, lang)