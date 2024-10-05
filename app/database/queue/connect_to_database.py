import asyncpg
import os

from dotenv import load_dotenv, find_dotenv


async def connect_to_database() -> asyncpg.connect | None:
    """
    Connects to the PostgreSQL database using environment variables.

    The environment variables 'POSTGRES_DB', 'POSTGRES_USER', and
    'POSTGRES_PASSWORD' must be set.

    Returns an asyncpg connection object.
    """
    try:
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
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None