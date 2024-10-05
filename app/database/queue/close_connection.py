async def close_connection(conn) -> bool:
    """
    Closes the connection to the database.

    Args:
        conn: The connection to be closed.

    Returns:
        bool: True if the connection was closed successfully, False if an error occurred.
    """
    await conn.close()
    return True