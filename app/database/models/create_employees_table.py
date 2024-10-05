from app.database.queue.close_connection import close_connection
from app.database.queue.connect_to_database import connect_to_database
from app.database.queue.add_telegram_id_unique_constraint import add_telegram_id_unique_constraint


async def create_employees_table() -> bool | None:
    """
    Create 'employees' table if it doesn't exist.

    Checks if 'employees' table already exists in the database. If it doesn't, creates it with the following columns:
    - id (SERIAL PRIMARY KEY)
    - telegram_id (INT)
    - chat_id (INT)
    - telegram_username (VARCHAR(255))
    - full_name (VARCHAR(255))
    - department (VARCHAR(255))
    - position (VARCHAR(255))
    - personnel_number (INT)
    - manager_level (INT) : non-manager employees have manager_level = 0, others - 1, 2, 3;
                            they get messages with correspoding risk level
    - rating (INT) with default value 0 : if has_one_rating_reset = True, rating = 0
    - is_in_antirating (BOOLEAN) with default value FALSE : employees that have not confirmed a risk when it reached
                                                            level 4 and the request was closed have is_in_antirating = True,
                                                            they get a disciplinary action and after that is_in_antirating = False
    - has_one_rating_reset (BOOLEAN) with default value FALSE : employees that have not confirmed a risk when it reached
                                                                level 4 and the request was closed have has_one_rating_reset = True
                                                                and is no longer changed
    - was_a_good_fellow (BOOLEAN) with default value FALSE : once every 14 days a good fellow is chosen among all employees,
                                                             when an employee is marked as good fellow, it is set to True,
                                                             and is no longer changed
    - banned (BOOLEAN) with default value FALSE : when has_one_rating_reset = True and bot tries to again set has_one_rating_reset = True,
                                                  banned = True and is no longer changed

    Also adds a unique constraint on telegram_id to prevent duplicate entries.

    Returns True if the table was created successfully, False otherwise, or None if an error occurred.
    """
    conn = await connect_to_database()
    try:
        result = await conn.fetchval("""
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_name = 'employees'
            );
        """)

        if result:
            print("Employees table already exists")
            return True

        await conn.execute("""CREATE TABLE IF NOT EXISTS employees (
                           id SERIAL PRIMARY KEY,
                           telegram_id INT,
                           chat_id INT,
                           telegram_username VARCHAR(255),
                           full_name VARCHAR(255),
                           department VARCHAR(255),
                           position VARCHAR(255),
                           personnel_number INT,
                           manager_level INT,
                           rating INT DEFAULT 0,
                           is_in_antirating BOOLEAN DEFAULT FALSE,
                           has_one_rating_reset BOOLEAN DEFAULT FALSE,
                           was_a_good_fellow BOOLEAN DEFAULT FALSE,
                           banned BOOLEAN DEFAULT FALSE
                           );
                           """)
        print("Employees table created successfully")

        add_constraint_result = await add_telegram_id_unique_constraint()

        if add_constraint_result is None:
            return False

        return True
    except Exception as e:
        print(f"Error creating Employees table: {e}")
        return None
    finally:
        if conn:
            await close_connection(conn)