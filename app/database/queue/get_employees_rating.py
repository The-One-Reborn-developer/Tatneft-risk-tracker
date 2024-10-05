from app.database.queue.connect_to_database import connect_to_database
from app.database.queue.close_connection import close_connection


async def get_employees_rating() -> list | None:
    """
    Get a list of employees with their names, departments, positions and ratings,
    sorted in descending order of rating.

    Returns:
        list | None: A list of dictionaries, each dictionary containing the full name,
            department, position and rating of an employee. If an error occurs,
            returns None.
    """
    conn = await connect_to_database()
    try:
        result = await conn.fetch(
            """
            SELECT
                full_name,
                department,
                position,
                rating
            FROM
                employees
            WHERE
                rating IS NOT NULL
            ORDER BY
                rating DESC
            """
        )

        return result
    except Exception as e:
        print(f"Error getting employees rating: {e}")
        return None
    finally:
        await close_connection(conn)