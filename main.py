from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from contextlib import asynccontextmanager
import asyncio

from childclass_queue import worker_queue, send_text_queue
from classes_ai import chat
from class_db import db
from read_scripts import read_file
from recog import vosk_recognize, active_sessions
from logicweb import handle_text, handle_audio, difference_account, session_succes



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
            data = await websocket.receive()
            
            if data["type"] == "websocket.disconnect":
                break

            if data.get("text"):
                await handle_text(websocket, data["text"])
                    
            elif data.get("bytes"):
                if websocket not in session_succes:
                    continue
                text = await asyncio.to_thread(vosk_recognize, websocket, data["bytes"])
                if text["text"] != "":
                    bool_handle_audio = await handle_audio(websocket, text)
                    if not bool_handle_audio:
                        break

            await difference_account(websocket)

    except WebSocketDisconnect:
        print("отключился")
    finally:
        if websocket in session_succes and session_succes[websocket].get("id"):
            if session_succes[websocket]["num"] >= session_succes[websocket]["num_succes"]:
                await db.execute(
                    "UPDATE players_stats SET calls = calls + 1, succ_calls = succ_calls + 1 WHERE user_id = $1",
                    session_succes[websocket]["id"]
                )
            else:
                await db.execute(
                    "UPDATE players_stats SET calls = calls + 1 WHERE user_id = $1",
                    session_succes[websocket]["id"]
                )
            del session_succes[websocket]
        if websocket in active_sessions:
            del active_sessions[websocket]
        await chat.clear_history(websocket)