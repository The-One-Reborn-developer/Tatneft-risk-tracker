from app.database.queue.connect_to_database import connect_to_database
from app.database.queue.close_connection import close_connection


async def get_all_level_three_managers() -> list | None:
    """
    Get a list of all chat IDs of level three managers.

    Returns a list of all chat IDs of level three managers if successful, None otherwise.
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
                manager_level = 3
            """
        )

        chat_ids = [manager['chat_id'] for manager in managers]
        print(f'Successfully fetched all level three managers: {chat_ids}')
        return chat_ids
    except Exception as e:
        print(f"Error getting all level three managers: {e}")
        return None
    finally:
        await close_connection(conn)