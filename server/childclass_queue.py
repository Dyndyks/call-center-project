import asyncio
from random import choice

from client_ai import get_otvet


class WebQueue(asyncio.Queue):
    def get_queue(self):
        return list(self._queue)


webqueue = WebQueue()

queue_responses = ["'звуки телевизора на фоне'", "'звуки разговоров на фоне'", "'звуки ветра'",
                    "'скрежет на фоне'", "звуки в дороге", "'щелканье мышкой'"]


async def send_text_queue():
    while True:
        for web in webqueue.get_queue():
            try:
                await web[0].send_text(choice(queue_responses))
            except:
                pass
        await asyncio.sleep(3)


async def worker_queue():
    while True:
        websocket, text, future = await webqueue.get()
        try:
            response = await get_otvet(websocket, text)
            future.set_result(response)
        except Exception as e:
            future.set_exception(e)
        finally:
            webqueue.task_done()


async def ask_worker_queue(websocket, text):
    future = asyncio.Future()
    await webqueue.put((websocket, text, future))
    return await future