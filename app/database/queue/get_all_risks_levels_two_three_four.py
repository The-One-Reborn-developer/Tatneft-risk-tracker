from typing import Literal

from app.database.queue.connect_to_database import connect_to_database
from app.database.queue.close_connection import close_connection


async def get_all_risks_levels_two_three_four() -> list[dict] | Literal[False] | None:
    """
    Get a list of all risks of level two, three and four.

    Returns a list of dictionaries, each dictionary containing the request number,
    risk level, claimant Telegram ID and performer Telegram ID of a risk if successful,
    False if no risks of level two, three and four were found, or None if an error occurred.
    """
    conn = None
    conn = await connect_to_database()
    try:
        risks = await conn.fetch(
            """
            SELECT
                request_number, risk_level, claimant_telegram_id, performer_telegram_id
            FROM
                risks
            WHERE
                risk_level IN (2, 3, 4)
            """
        )

        if not risks:
            print("No risks of level two, three and four found")
            return False
        
        risk_data = [
            {
                'request_number': risk['request_number'],
                'risk_level': risk['risk_level'],
                'claimant_telegram_id': risk['claimant_telegram_id'],
                'performer_telegram_id': risk['performer_telegram_id']
            }
            for risk in risks
        ]

        print(f'Successfully fetched all risks of level two, three, and four: {risk_data}')
        return risk_data
    except Exception as e:
        print(f"Error getting all risks of level two, three and four: {e}")
        return None
    finally:
        if conn:
            await close_connection(conn)