from datetime import datetime, timedelta
from typing import List
import sqlite3
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE_DIR, "appointments.db")


# -------------------------
# DB INIT
# -------------------------
def init_db():
    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id TEXT,
                doctor_id TEXT,
                start_ts INTEGER,
                end_ts INTEGER,
                status TEXT
            )
            """
        )
        conn.commit()


# -------------------------
# UTIL
# -------------------------
def _overlaps(a_start, a_end, b_start, b_end):
    return a_start < b_end and b_start < a_end


def _is_working_hours(start_ts: int):
    dt = datetime.fromtimestamp(start_ts)
    return 9 <= dt.hour < 17  # 9 AM – 5 PM


# -------------------------
# CONFLICT CHECK
# -------------------------
def find_conflicts(doctor_id: str, start_ts: int, end_ts: int) -> List[dict]:
    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        c.execute(
            """
            SELECT id, patient_id, start_ts, end_ts, status 
            FROM appointments 
            WHERE doctor_id=? AND status='booked'
            """,
            (doctor_id,)
        )
        rows = c.fetchall()

    conflicts = []
    for r in rows:
        if _overlaps(start_ts, end_ts, r[2], r[3]):
            conflicts.append({
                "id": r[0],
                "patient_id": r[1],
                "start_ts": r[2],
                "end_ts": r[3]
            })

    return conflicts


# -------------------------
# SUGGEST ALTERNATIVES
# -------------------------
def suggest_alternatives(doctor_id: str, start_ts: int) -> List[int]:
    alternatives = []
    base = datetime.fromtimestamp(start_ts)

    for i in range(1, 4):  # next 3 slots
        new_time = base + timedelta(minutes=30 * i)
        s = int(new_time.timestamp())
        e = s + 15 * 60

        if _is_working_hours(s) and not find_conflicts(doctor_id, s, e):
            alternatives.append(s)

    return alternatives


# -------------------------
# BOOK APPOINTMENT
# -------------------------
def book_appointment(patient_id: str, doctor_id: str, start_ts: int, end_ts: int) -> dict:

    now_ts = int(datetime.now().timestamp())

    # ❌ Past time
    if start_ts < now_ts:
        return {"ok": False, "reason": "past_time"}

    # ❌ Invalid time
    if end_ts <= start_ts:
        return {"ok": False, "reason": "invalid_time"}

    # ❌ Outside working hours
    if not _is_working_hours(start_ts):
        return {"ok": False, "reason": "outside_working_hours"}

    # ❌ Conflict
    conflicts = find_conflicts(doctor_id, start_ts, end_ts)
    if conflicts:
        return {
            "ok": False,
            "reason": "conflict",
            "alternatives": suggest_alternatives(doctor_id, start_ts)
        }

    # ✅ Insert booking
    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        c.execute(
            """
            INSERT INTO appointments 
            (patient_id, doctor_id, start_ts, end_ts, status) 
            VALUES (?, ?, ?, ?, ?)
            """,
            (patient_id, doctor_id, start_ts, end_ts, "booked")
        )
        conn.commit()
        appt_id = c.lastrowid

    return {"ok": True, "id": appt_id}


# -------------------------
# CANCEL
# -------------------------
def cancel_appointment(appt_id: int) -> bool:
    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        c.execute(
            "UPDATE appointments SET status='cancelled' WHERE id=?",
            (appt_id,)
        )
        conn.commit()
        return c.rowcount > 0