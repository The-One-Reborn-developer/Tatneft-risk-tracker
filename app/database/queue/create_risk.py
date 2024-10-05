import datetime

from app.database.queue.connect_to_database import connect_to_database
from app.database.queue.close_connection import close_connection


async def create_risk(risk) -> bool | None:
    """
    Add a risk to the database.

    Parameters
    ----------
    risk : dict
        A dictionary with the following keys:
            telegram_id : int
                The Telegram ID of the employee who discovered the risk.
            discovery_date : str
                The date of risk discovery in the format '%Y-%m-%d'.
            risk_type : str
                The type of risk.
            risk_description : str
                A description of the risk.
            request_number : int
                The number of the request corresponding with the risk in IntraService.

    Returns
    -------
    bool
        True if the risk was added successfully, None if an error occurred.
    """
    conn = await connect_to_database()
    # Convert discovery_date from string to datetime.date
    discovery_date = datetime.datetime.strptime(risk['discovery_date'], '%Y-%m-%d').date()
    try:
        await conn.execute(
            """
            INSERT INTO risks
            (telegram_id,
            discovery_date,
            risk_type,
            risk_description,
            request_number)
            VALUES
            ($1, $2, $3, $4, $5)
            """,
            risk['telegram_id'],
            discovery_date,
            risk['risk_type'],
            risk['risk_description'],
            risk['request_number']
        )

        print(f'Risk {risk["request_number"]} discovered by {risk["telegram_id"]} at {discovery_date} added successfully.')
        return True
    except Exception as e:
        print(f"Error adding risk: {e}")
        return None
    finally:
        await close_connection(conn)