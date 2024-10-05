from typing import Literal

from app.database.queue.close_connection import close_connection
from app.database.queue.connect_to_database import connect_to_database


async def create_risks_table() -> Literal[True] | None:
    """
    Create 'risks' table if it doesn't exist.

    Checks if 'risks' table already exists in the database. If it doesn't, creates it with the following columns:
    - id (SERIAL PRIMARY KEY)
    - claimant_telegram_id (INT) REFERENCES employees(telegram_id) ON DELETE CASCADE : the employee who submitted the request
    - performer_telegram_id (INT) REFERENCES employees(telegram_id) ON DELETE CASCADE : the employee who resolves the request
    - discovery_date (DATE) : MSK time
    - discovery_time (TIME) : MSK time
    - confirmation_date (DATE) with default value of NULL : MSK time
    - elimination_date (DATE) with default value of NULL : MSK time
    - risk_level (INT) with default value of 1
    - risk_type (VARCHAR(255))
    - risk_description (TEXT)
    - risk_confirmed (BOOLEAN) with default value of NULL
    - risk_eliminated (BOOLEAN) with default value of FALSE
    - request_number (INT) : IntraService ticket number
    - request_closed (BOOLEAN) with default value of FALSE

    Returns True if the table was created successfully, None otherwise.
    """
    conn = None
    conn = await connect_to_database()
    try:
        result = await conn.fetchval("""
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_name = 'risks'
            );
        """)

        if result:
            print("Risks table already exists")
            return True

        await conn.execute("""CREATE TABLE IF NOT EXISTS risks (
                           id SERIAL PRIMARY KEY,
                           claimant_telegram_id INT REFERENCES employees(telegram_id) ON DELETE CASCADE,
                           performer_telegram_id INT REFERENCES employees(telegram_id) ON DELETE CASCADE,
                           discovery_date DATE,
                           discovery_time TIME,
                           confirmation_date DATE DEFAULT NULL,
                           elimination_date DATE DEFAULT NULL,
                           risk_level INT DEFAULT 1,
                           risk_type VARCHAR(255),
                           risk_description TEXT,
                           risk_confirmed BOOLEAN DEFAULT NULL,
                           risk_eliminated BOOLEAN DEFAULT FALSE,
                           request_number INT,
                           request_closed BOOLEAN DEFAULT FALSE
                           );
                           """)
        print("Risks table created successfully")
        return True
    except Exception as e:
        print(f"Error creating Risks table: {e}")
        return None
    finally:
        if conn:
            await close_connection(conn)