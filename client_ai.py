from gigachat import GigaChatAsyncClient
from gigachat.models import Chat

import asyncio

from classes_ai import GigaToken, chat

from config import CLIENT_ID, CLIENT_SECRET



giga_tk = GigaToken(CLIENT_ID, CLIENT_SECRET)

queue = asyncio.Queue()
    

async def get_otvet(websocket, text):
    """
    из самого юнити клиента получать именно: что надо/процент и само сообщение
    """
    token = await giga_tk.get_tk()
    async with GigaChatAsyncClient(
        base_url="https://api.giga.chat/v1",
        model="GigaChat-2",
        access_token=token,
        scope="GIGACHAT_API_PERS",
    ) as giga:
        
        await chat.add_history(websocket, "user", text)
        
        messages = Chat(messages=await chat.get_history(websocket))

        response = await giga.achat(messages)

        await chat.add_history(websocket, "assistant", response.choices[0].message.content)
        return response.choices[0].message.content


async def worker():
    while True:
        websocket, text, future = await queue.get()
        try:
            response = await get_otvet(websocket, text)
            future.set_result(response)
        except Exception as e:
            future.set_exception(e)
        finally:
            queue.task_done()


async def ask_worker(websocket, text):
    future = asyncio.Future()
    await queue.put((websocket, text, future))
    return await future