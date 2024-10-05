from app.database.queue.connect_to_database import connect_to_database
from app.database.queue.close_connection import close_connection


async def get_all_level_one_managers() -> list | None:
    """
    Get a list of Telegram chat IDs of all employees with manager level 1.

    Returns a list of dictionaries, each dictionary containing the 'chat_id' of a level 1 manager.
    If an error occurs, returns None.
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
        await close_connection(conn)