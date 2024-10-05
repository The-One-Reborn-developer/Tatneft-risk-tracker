from app.database.queue.connect_to_database import connect_to_database
from app.database.queue.close_connection import close_connection


async def get_all_risks_levels_two_three_four() -> list | None:
    """
    Get a list of all request_number of risks of level two, three and four.

    Returns a list of all request_number of risks of level two, three and four if successful, None if an error occurred.
    """
    conn = None
    conn = await connect_to_database()
    try:
        risks = await conn.fetch(
            """
            SELECT
                request_number
            FROM
                risks
            WHERE
                risk_level IN (2, 3, 4)
            """
        )

        request_numbers = [risk['request_number'] for risk in risks]

        if not request_numbers:
            print("No risks of level two, three and four found")
            return []

        print(f'Successfully fetched all risks of level two, three and four: {request_numbers}')
        return request_numbers
    except Exception as e:
        print(f"Error getting all risks of level two, three and four: {e}")
        return None
    finally:
        if conn:
            await close_connection(conn)