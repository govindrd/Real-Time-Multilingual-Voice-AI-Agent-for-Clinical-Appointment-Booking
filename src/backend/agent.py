import os
import time
import logging
from datetime import datetime, timedelta

from .memory import memory
from .scheduler import book_appointment, find_conflicts

logger = logging.getLogger(__name__)


# -------------------------
# NLU
# -------------------------
async def nlu_parse(text: str, lang: str = "en") -> dict:
    text_l = text.lower()

    if "book" in text_l or "schedule" in text_l:
        return {"intent": "book", "slots": {}}
    if "yes" in text_l or "confirm" in text_l:
        return {"intent": "confirm", "slots": {}}
    if "cancel" in text_l:
        return {"intent": "cancel", "slots": {}}

    return {"intent": "unknown", "slots": {}}


# -------------------------
# SMART SLOT GENERATION
# -------------------------
def get_next_available_slot():
    now = datetime.now()

    # Try multiple time slots
    for hour in [10, 11, 12, 14, 15]:
        slot = now + timedelta(days=1)
        slot = slot.replace(hour=hour, minute=0, second=0)

        start_ts = int(slot.timestamp())
        end_ts = start_ts + 15 * 60

        conflicts = find_conflicts("dr_1", start_ts, end_ts)

        if not conflicts:
            return start_ts, end_ts

    return None, None


# -------------------------
# MAIN AGENT
# -------------------------
async def handle_text(session_id: str, text: str, lang: str = "en") -> dict:
    start = time.time()

    session = memory.get_session(session_id) or {}

    parsed = await nlu_parse(text, lang)
    intent = parsed.get("intent")

    # -------------------------
    # BOOK FLOW
    # -------------------------
    if intent == "book":
        start_ts, end_ts = get_next_available_slot()

        if not start_ts:
            text_out = "Sorry, no slots available tomorrow."
        else:
            memory.update_session(session_id, {
                "pending_booking": {
                    "doctor_id": "dr_1",
                    "start_ts": start_ts,
                    "end_ts": end_ts
                }
            })

            readable = datetime.fromtimestamp(start_ts).strftime("%I:%M %p")
            text_out = f"I found a slot tomorrow at {readable}. Do you want to confirm?"

    # -------------------------
    # CONFIRM FLOW
    # -------------------------
    elif intent == "confirm":
        pending = session.get("pending_booking")

        if not pending:
            text_out = "No active booking found. Please start again."
        else:
            res = book_appointment(
                patient_id=session_id,
                doctor_id=pending["doctor_id"],
                start_ts=pending["start_ts"],
                end_ts=pending["end_ts"]
            )

            if res.get("ok"):
                memory.update_session(session_id, {"pending_booking": None})
                text_out = f"Your appointment is confirmed. ID: {res['id']}"
            else:
                # Try another slot automatically
                start_ts, end_ts = get_next_available_slot()

                if start_ts:
                    memory.update_session(session_id, {
                        "pending_booking": {
                            "doctor_id": "dr_1",
                            "start_ts": start_ts,
                            "end_ts": end_ts
                        }
                    })

                    readable = datetime.fromtimestamp(start_ts).strftime("%I:%M %p")
                    text_out = f"That slot was taken. I can offer {readable}. Do you want to confirm?"
                else:
                    text_out = "No alternative slots available."

    # -------------------------
    # CANCEL
    # -------------------------
    elif intent == "cancel":
        memory.clear_session(session_id)
        text_out = "Your session has been cleared."

    # -------------------------
    # UNKNOWN
    # -------------------------
    else:
        text_out = "Do you want to book, cancel, or reschedule an appointment?"

    latency = (time.time() - start) * 1000
    logger.info("Agent latency: %.1f ms", latency)

    return {
        "text": text_out,
        "meta": {
            "intent": intent,
            "latency_ms": latency
        }
    }