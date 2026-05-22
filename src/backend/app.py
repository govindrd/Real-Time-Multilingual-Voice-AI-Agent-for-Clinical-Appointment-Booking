import os
import time
import json
import logging
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from .logging_config import setup_logging
from .agent import handle_text
from .tts import synthesize_text_to_mp3_bytes
from .scheduler import init_db

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI()

init_db()

@app.get("/")
async def index():
    return HTMLResponse("<h3>Realtime Voice Agent backend</h3>")


@app.websocket('/ws/audio')
async def ws_audio(ws: WebSocket):
    await ws.accept()
    session_id = None
    try:
        while True:
            data = await ws.receive_text()
            msg = json.loads(data)
            # Demo-control messages: {type: 'speech_end', transcript: '...', session_id: '...'}
            if msg.get('type') == 'start_session':
                session_id = msg.get('session_id')
                await ws.send_text(json.dumps({'event': 'session_started', 'session_id': session_id}))
                continue
            if msg.get('type') == 'speech_end':
                recv_ts = time.time()
                transcript = msg.get('transcript')
                lang = msg.get('lang', 'en')
                # Measure end-to-first-audio latency: start timer now
                t0 = time.time()
                agent_res = await handle_text(session_id or 'anon', transcript, lang)
                response_text = agent_res['text']
                mp3_bytes = synthesize_text_to_mp3_bytes(response_text, lang=lang)
                t1 = time.time()
                latency_ms = (t1 - t0) * 1000
                logger.info('Speech-end to first audio latency: %.1fms', latency_ms)
                # Send metadata then base64 audio
                await ws.send_text(json.dumps({'event': 'response_meta', 'meta': {'latency_ms': latency_ms, 'agent_meta': agent_res['meta']}}))
                # For demo, send audio as base64 to keep websocket simple
                import base64
                await ws.send_text(json.dumps({'event': 'audio_base64', 'data': base64.b64encode(mp3_bytes).decode('ascii')}))
                continue
            # Keep-alives and other messages
            await ws.send_text(json.dumps({'event': 'echo', 'msg': msg}))
    except Exception as e:
        logger.exception('ws_audio error')
