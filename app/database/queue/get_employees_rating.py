from app.database.queue.connect_to_database import connect_to_database
from app.database.queue.close_connection import close_connection


async def get_employees_rating() -> list | None:
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