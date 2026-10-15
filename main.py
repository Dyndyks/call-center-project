from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from contextlib import asynccontextmanager
import asyncio

from client_ai import ask_worker
from classes_ai import chat
from class_db import db
from read_scripts import read_file
from client_ai import worker


class UserName(BaseModel):
    name: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await db.connect()
        task = asyncio.create_task(worker())
        yield
    except Exception as e:
        print(e)
    finally:
        task.cancel()
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
            data = await websocket.receive_text()
            
            otvet = await ask_worker(websocket, data)
            await websocket.send_text(otvet)
    except WebSocketDisconnect:
        print("отсоединился")
    finally:
        await chat.clear_history(websocket)