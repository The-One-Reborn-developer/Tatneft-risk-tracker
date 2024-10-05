from app.database.queue.connect_to_database import connect_to_database
from app.database.queue.close_connection import close_connection


async def get_all_level_two_managers() -> list | None:
    """
    Get a list of all chat IDs of level two managers.

    Returns a list of all chat IDs of level two managers if successful, None if an error occurred.
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
                manager_level = 2
            """
        )

        chat_ids = [manager['chat_id'] for manager in managers]
        print(f'Successfully fetched all level two managers: {chat_ids}')
        return chat_ids
    except Exception as e:
        print(f"Error getting all level two managers: {e}")
        return None
    finally:
        await close_connection(conn)