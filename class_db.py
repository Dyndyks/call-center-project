import asyncpg
from config import USER, PASSWORD, PORT


class DBMeneger():

    def __init__(self):
        self.pool = None

    async def connect(self):
        await check_db()
        self.pool = await asyncpg.create_pool(
            user=USER,
            password=PASSWORD,
            database="call_center_db",
            host="localhost",
            port=PORT
        )

        await self._init_table()

    async def db_close(self):
        if self.pool is not None:
            await self.pool.close()

    async def execute(self, query, *args):
        async with self.pool.acquire() as conn:
            await conn.execute(query, *args)

    async def fetchval(self, query, *args):
        async with self.pool.acquire() as conn:
            await conn.fetchval(query, *args)

    async def _init_table(self):
        async with self.pool.acquire() as conn:
            await conn.execute("""
CREATE TABLE IF NOT EXISTS players(
id SERIAL PRIMARY KEY,
username TEXT NOT NULL UNIQUE
)
"""
                               )

            await conn.execute("""
CREATE TABLE IF NOT EXISTS players_stats(
id SERIAL PRIMARY KEY,
user_id INTEGER REFERENCES players(id) ON DELETE CASCADE,
calls INTEGER DEFAULT 0,
succ_calls INTEGER DEFAULT 0
)
"""
                               )


async def check_db():

    conn = await asyncpg.connect(
        user=USER,
        password=PASSWORD,
        database="postgres",
        host="localhost",
        port=PORT
    )
    exist_base = await conn.fetchrow(
        "SELECT 1 FROM pg_database WHERE datname = $1",
        "call_center_db"
    )

    if exist_base is None:
        await conn.execute("CREATE DATABASE call_center_db")

    await conn.close()


db = DBMeneger()