import aiofiles
import json
import os
import asyncio
from random import choice


async def get_random_file():
    files = await asyncio.to_thread(os.listdir, "SalesScripts")
    files_json = [f for f in files if f.endswith(".json")]
    return choice(files_json)


async def read_file():
    file = await get_random_file()
    async with aiofiles.open(f"SalesScripts/{file}", "r", encoding="utf-8") as f:
        meta = json.loads(await f.read())

    name_file = meta["file"]
    async with aiofiles.open(f"SalesScripts/{name_file}", "r", encoding="utf-8") as f:
        return {"script": await f.read(), "name_file": file}


async def get_succes(file):
    async with aiofiles.open(f"SalesScripts/{file}", "r", encoding="utf-8") as f:
        meta = json.loads(await f.read())
    return meta["succes"]