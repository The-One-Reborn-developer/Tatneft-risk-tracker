from typing import Literal

from app.database.queue.connect_to_database import connect_to_database
from app.database.queue.close_connection import close_connection


async def update_employee(telegram_id: int, **kwargs) -> Literal[True] | None:
    """
    Update an employee in the database.

    Args:
        telegram_id: The Telegram ID of the employee to update.
        **kwargs: Dynamic fields for updating the employee. 
                  Allowed keys are: 'rating', 'is_in_antirating', 'has_one_rating_reset', 'was_a_good_fellow', 'banned'.

    Returns:
        True if the employee was updated successfully, None if an error occurred.
    """
    conn = None
    conn = await connect_to_database()
    try:
        # Filter out fields that are None (we don't want to update these)
        update_fields = {key: value for key, value in kwargs.items() if value is not None}
        
        # Ensure there is at least one field to update
        if not update_fields:
            print(f"No fields to update for employee with Telegram ID {telegram_id}.")
            return True
        
        # Dynamically build the SQL query
        set_clause = ", ".join([f"{field} = ${i+1}" for i, field in enumerate(update_fields.keys())])
        values = list(update_fields.values()) + [telegram_id]

        # Add explicit type casting for None values in PostgreSQL
        query = f"""
        UPDATE employees
        SET {set_clause}
        WHERE telegram_id = ${len(values)}
        """
        
        # Log the query and values for debugging
        print(f"Executing query: {query} with values: {values}")

        await conn.execute(query, *values)

        print(f"Employee with Telegram ID {telegram_id} updated successfully.")
        return True
    except Exception as e:
        print(f"Error updating employee: {e}")
        return None
    finally:
        if conn:
            await close_connection(conn)
