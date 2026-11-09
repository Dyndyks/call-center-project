import json
import re
from read_scripts import get_succes
from childclass_queue import ask_worker_queue


session_succes = {}


async def handle_text(websocket, json_message):
    message = json.loads(json_message)
    if message["type"] == "file":
        if websocket not in session_succes:
            session_succes[websocket] = {"num_succes": await get_succes(message["text"]), "num": 0}
    if message["type"] == "id":
        session_succes[websocket]["id"] = int(message["text"])


async def handle_audio(websocket, vosk_text):
    if not vosk_text["final"]:
        result = vosk_text["text"]
        await websocket.send_json({"type": "я", "text": result})
    elif vosk_text["final"]:
        result = vosk_text["text"]
        await websocket.send_json({"type": "я", "text": result})
        otvet_ai = await ask_worker_queue(websocket, vosk_text["text"])
        if re.search(r"\bда\b", otvet_ai, re.IGNORECASE) is not None:
            session_succes[websocket]["num"] += 1
        elif re.search(r"\bнет\b", otvet_ai, re.IGNORECASE) is not None:
            session_succes[websocket]["num"] -= 1
        elif re.search(r"\bсброс\b", otvet_ai, re.IGNORECASE):
            await websocket.send_json({"type": "сброс", "text": otvet_ai})
            return False
        await websocket.send_json({"type": "клиент", "text": otvet_ai})
    return True


async def difference_account(websocket):
    num, num_succes = session_succes[websocket]["num"], session_succes[websocket]["num_succes"]
    color = "red"
    if num >= num_succes:
        color = "green"
    await websocket.send_json({"type": "total_succes", "text": f"<color={color}>{str(num)}/{str(num_succes)}</color>"})