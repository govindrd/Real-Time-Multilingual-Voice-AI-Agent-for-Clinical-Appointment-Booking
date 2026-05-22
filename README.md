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

