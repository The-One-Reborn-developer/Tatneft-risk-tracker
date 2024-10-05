from app.database.queue.connect_to_database import connect_to_database
from app.database.queue.close_connection import close_connection


async def get_all_level_one_managers() -> list | None:
    """
    Get a list of all chat IDs of level one managers.

    Returns a list of all chat IDs of level one managers if successful, None if an error occurred.
    """
    conn = await connect_to_database()
    try:
        managers = await conn.fetch(
            """
            SELECT
                chat_id
            FROM
                employees
            WHERE
                manager_level = 1
            """
        )

        chat_ids = [manager['chat_id'] for manager in managers]
        print(f'Successfully fetched all level one managers: {chat_ids}')
        return chat_ids
    except Exception as e:
        print(f"Error getting all level one managers: {e}")
        return None
    finally:
        if conn:
            await close_connection(conn)