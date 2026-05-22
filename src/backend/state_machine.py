# backend/state_machine.py

class ConversationState:
    def __init__(self):
        self.state = "IDLE"

        # booking context
        self.doctor = None
        self.start_ts = None
        self.end_ts = None

        # flags
        self.awaiting_confirmation = False
        self.last_intent = None

    # -------------------------
    # STATE TRANSITIONS
    # -------------------------
    def transition(self, intent: str):
        self.last_intent = intent

        # -------------------------
        # BOOK FLOW
        # -------------------------
        if intent == "book":
            self.state = "BOOKING"
            self.awaiting_confirmation = True

        elif intent == "confirm" and self.awaiting_confirmation:
            self.state = "CONFIRMED"
            self.awaiting_confirmation = False

        # -------------------------
        # CANCEL FLOW
        # -------------------------
        elif intent == "cancel":
            self.state = "CANCELLED"
            self.reset()

        # -------------------------
        # RESCHEDULE FLOW
        # -------------------------
        elif intent == "reschedule":
            self.state = "RESCHEDULING"
            self.awaiting_confirmation = True

        # -------------------------
        # UNKNOWN / FALLBACK
        # -------------------------
        else:
            self.state = "IDLE"

    # -------------------------
    # RESET STATE
    # -------------------------
    def reset(self):
        self.doctor = None
        self.start_ts = None
        self.end_ts = None
        self.awaiting_confirmation = False
        self.last_intent = None

    # -------------------------
    # SERIALIZATION (IMPORTANT)
    # -------------------------
    def to_dict(self):
        return {
            "state": self.state,
            "doctor": self.doctor,
            "start_ts": self.start_ts,
            "end_ts": self.end_ts,
            "awaiting_confirmation": self.awaiting_confirmation,
            "last_intent": self.last_intent
        }

    @classmethod
    def from_dict(cls, data: dict):
        obj = cls()
        obj.state = data.get("state", "IDLE")
        obj.doctor = data.get("doctor")
        obj.start_ts = data.get("start_ts")
        obj.end_ts = data.get("end_ts")
        obj.awaiting_confirmation = data.get("awaiting_confirmation", False)
        obj.last_intent = data.get("last_intent")
        return obj