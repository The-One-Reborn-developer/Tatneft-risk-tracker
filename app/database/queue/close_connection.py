async def close_connection(conn) -> bool:
    await conn.close()
    return True