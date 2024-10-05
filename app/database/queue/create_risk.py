import datetime

from app.database.queue.connect_to_database import connect_to_database
from app.database.queue.close_connection import close_connection


async def add_risk(risk) -> bool:
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

        print(f'Risk {risk["request_number"]} by {risk["telegram_id"]} discovered at {discovery_date} added successfully.')
        return True
    except Exception as e:
        print(f"Error adding risk: {e}")
        return False
    finally:
        await close_connection(conn)