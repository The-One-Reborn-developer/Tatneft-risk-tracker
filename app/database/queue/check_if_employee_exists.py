from app.database.queue.connect_to_database import connect_to_database
from app.database.queue.close_connection import close_connection


async def check_if_employee_exists(telegram_id: int) -> bool:
    """
    Check if an employee with the given Telegram ID exists in the database.

    Args:
        telegram_id: The Telegram ID of the employee to check.

    Returns:
        bool: True if the employee exists, False otherwise.
    """
    conn = await connect_to_database()
    try:
        result = await conn.fetchval(
            """
            SELECT
                EXISTS (
                    SELECT
                        1
                    FROM
                        employees
                    WHERE
                        telegram_id = $1
                )
            """,
            telegram_id,
        )

        if result:
            print(f"Employee with Telegram ID {telegram_id} exists in the database.")
            return True
        else:
            print(f"Employee with Telegram ID {telegram_id} does not exist in the database.")
            return False
    except Exception as e:
        print(f"Error checking if employee exists: {e}")
    finally:
        await close_connection(conn)