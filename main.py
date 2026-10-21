from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from contextlib import asynccontextmanager
import asyncio

from childclass_queue import ask_worker_queue, worker_queue, send_text_queue
from classes_ai import chat
from class_db import db
from read_scripts import read_file
from recog import vosk_recognize, active_sessions



class UserName(BaseModel):
    name: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await db.connect()
        task_worker_queue = asyncio.create_task(worker_queue())
        task_send_text_queue = asyncio.create_task(send_text_queue())
        yield
    except Exception as e:
        print(e)
    finally:
        task_send_text_queue.cancel()
        task_worker_queue.cancel()
        await db.close()



app = FastAPI(lifespan=lifespan)


@app.post("/user")
async def check_create_user(data: UserName):
    username = data.name
    user_id = await db.fetchval(
        "SELECT id FROM players WHERE username = $1", username
    )

    if user_id is None:
        user_id = await db.fetchval(
            "INSERT INTO players (username) VALUES ($1) RETURNING id", username
        )
        await db.execute(
            "INSERT INTO players_stats (user_id) VALUES ($1)", user_id
        )
    return {"user_id": user_id, "user_name": username}


@app.get("/stats")
async def send_stats(user_id: int):
    stats = await db.fetchrow(
        "SELECT * FROM players_stats WHERE user_id = $1", user_id
    )
    result = dict(stats)
    del result["id"]
    del result["user_id"]
    return result


@app.get("/script")
async def send_sript():
    return await read_file()


@app.websocket("/dialog")
async def dialog(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_bytes()
            text = await asyncio.to_thread(vosk_recognize, websocket, data)
            if text["text"] != "":
                if not text["final"]:
                    await websocket.send_text(text["text"])
                if text["final"]:
                    await websocket.send_text(text["text"])
                    otvet_ai = await ask_worker_queue(websocket, text["text"])
                    await websocket.send_text(otvet_ai)
    except WebSocketDisconnect:
        del active_sessions[websocket]
        print("отсоединился")
    finally:
        await chat.clear_history(websocket)