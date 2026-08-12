from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
import requests

from client_ai import get_otvet



class Dialog(BaseModel):
    operator: str
    client: str


app = FastAPI()


@app.get("/")
async def root():
    return "connect"


@app.websocket("/dialog")
async def dialog(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            
            otvet = await get_otvet(data)
            await websocket.send_text(otvet)
    except WebSocketDisconnect:
        print("отсоединился")