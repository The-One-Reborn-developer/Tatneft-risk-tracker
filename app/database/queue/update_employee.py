from typing import Literal

from app.database.queue.connect_to_database import connect_to_database
from app.database.queue.close_connection import close_connection


async def update_employee(telegram_id: int,
                          rating: int | None = None,
                          is_in_antirating: bool | None = None,
                          has_one_rating_reset: bool | None = None,
                          was_a_good_fellow: bool | None = None,
                          banned: bool | None = None) -> Literal[True] | None:
    """
    Update an employee in the database.

    Args:
        telegram_id: The Telegram ID of the employee to update.
        rating: The new rating of the employee.
        is_in_antirating: Whether the employee is in anti-rating.
        has_one_rating_reset: Whether the employee has had one rating reset.
        was_a_good_fellow: Whether the employee was a good fellow.
        banned: Whether the employee is banned.

    Returns:
        bool: True if the employee was updated successfully, None if an error occurred.
    """
    conn = None
    conn = await connect_to_database()
    try:
        if rating:
            await conn.execute(
                """
                UPDATE
                    employees
                SET
                    rating = $1,
                    is_in_antirating = $2,
                    has_one_rating_reset = $3,
                    was_a_good_fellow = $4,
                    banned = $5
                WHERE
                    telegram_id = $6
                """,
                rating,
                is_in_antirating,
                has_one_rating_reset,
                was_a_good_fellow,
                banned,
                telegram_id
            )

        print(f"Employee with Telegram ID {telegram_id} updated successfully.")
        return True
    except Exception as e:
        print(f"Error updating employee: {e}")
        return None
    finally:
        if conn:
            await close_connection(conn)