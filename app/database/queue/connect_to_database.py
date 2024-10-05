import asyncpg
import os

from dotenv import load_dotenv, find_dotenv


async def connect_to_database() -> asyncpg.connect:
    load_dotenv(find_dotenv())

    database = os.getenv("POSTGRES_DB")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")

    conn = await asyncpg.connect(
        host="localhost",
        database=database,
        user=user,
        password=password
    )
    return conn