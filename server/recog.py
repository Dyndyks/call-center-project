from vosk import Model, KaldiRecognizer
import json

model = Model("../models/vosk-model-small-ru-0.22")
active_sessions = {}

def vosk_recognize(websocket, audio_bytes):
    if websocket not in active_sessions:
        active_sessions[websocket] = KaldiRecognizer(model, 16000)

    rec = active_sessions[websocket]

    if rec.AcceptWaveform(audio_bytes):
        result = json.loads(rec.Result())
        return {"text": result.get("text", ""), "final": True}
    else:
        partial = json.loads(rec.PartialResult())
        return {"text": partial.get("partial", ""), "final": False}