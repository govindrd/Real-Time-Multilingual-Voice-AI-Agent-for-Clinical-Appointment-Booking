# 🎤 Real-Time Multilingual Voice AI Agent — Clinical Appointments

This project implements a **real-time voice AI agent** for booking and managing clinical appointments through natural conversations.

The system is designed to handle **end-to-end voice interactions** — from speech input to intelligent decision-making and voice responses — with a strong focus on **low latency (<450ms), agent orchestration, and real-world scheduling constraints**.

---

## 🚀 Key Capabilities

- 🎤 **Voice-first interaction**
  - Accepts speech input and responds in natural voice
  - Supports real-time WebSocket communication

- 🌐 **Multilingual support**
  - English, Hindi, Tamil
  - Language preference persists across sessions

- 🧠 **Agentic reasoning**
  - Intent detection + slot extraction
  - Tool-based execution (booking, rescheduling, cancellation)
  - Multi-turn conversation handling via state machine

- 🗂️ **Contextual memory**
  - Session memory (Redis with TTL)
  - Persistent user context across sessions

- 📅 **Appointment scheduling engine**
  - Conflict detection (interval overlap)
  - Working hours enforcement
  - Alternative slot suggestions

- 📞 **Outbound campaign support**
  - Reminder calls and follow-ups (extensible via scheduler)

---

## 🏗️ System Architecture

```plaintext
User Speech
   ↓
Streaming ASR (Speech-to-Text)
   ↓
Agent (NLU + State Machine + Tools)
   ↓
Scheduler (Conflict Detection + Booking Logic)
   ↓
Response Generation
   ↓
TTS (Text-to-Speech)
   ↓
Audio Response (WebSocket)


<img width="1913" height="1007" alt="Screenshot 2026-05-22 125950" src="https://github.com/user-attachments/assets/551d8777-1ed2-42cb-8e19-7be7ad9426d0" />

<img width="869" height="346" alt="Screenshot 2026-05-22 125839" src="https://github.com/user-attachments/assets/94876eb5-5a2c-4d87-9474-63186247b977" />

<img width="1919" height="882" alt="Screenshot 2026-05-22 131335" src="https://github.com/user-attachments/assets/63cb4db0-f802-43fb-887a-7d096d95e4fa" />


<img width="1890" height="989" alt="Screenshot 2026-05-22 132701" src="https://github.com/user-attachments/assets/2be158bd-3682-45ac-b9be-474230260d7e" />

<img width="1606" height="533" alt="Screenshot 2026-05-22 133542" src="https://github.com/user-attachments/assets/7f29fed0-12a1-4749-842c-52afa33b6244" />

