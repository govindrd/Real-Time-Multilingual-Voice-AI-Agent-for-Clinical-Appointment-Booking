# backend/tools.py

from datetime import datetime
from .scheduler import book_appointment, find_conflicts, suggest_alternatives


# -------------------------
# CHECK AVAILABILITY
# -------------------------
def check_availability(doctor_id: str, start_ts: int, end_ts: int):
    conflicts = find_conflicts(doctor_id, start_ts, end_ts)
    return len(conflicts) == 0


# -------------------------
# BOOK TOOL
# -------------------------
def book_tool(patient_id: str, doctor_id: str, start_ts: int, end_ts: int):
    result = book_appointment(
        patient_id=patient_id,
        doctor_id=doctor_id,
        start_ts=start_ts,
        end_ts=end_ts
    )

    if result["ok"]:
        return {
            "status": "success",
            "message": f"Appointment booked successfully. ID: {result['id']}"
        }

    # handle conflicts
    if result["reason"] == "conflict":
        alternatives = result.get("alternatives", [])

        readable = [
            datetime.fromtimestamp(ts).strftime("%I:%M %p")
            for ts in alternatives
        ]

        return {
            "status": "conflict",
            "message": f"Slot unavailable. Try: {readable}"
        }

    return {
        "status": "error",
        "message": f"Booking failed: {result['reason']}"
    }


# -------------------------
# SUGGEST TOOL
# -------------------------
def suggest_tool(doctor_id: str, start_ts: int):
    alternatives = suggest_alternatives(doctor_id, start_ts)

    return [
        datetime.fromtimestamp(ts).strftime("%I:%M %p")
        for ts in alternatives
    ]