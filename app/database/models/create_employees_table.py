from app.database.queue.close_connection import close_connection
from app.database.queue.connect_to_database import connect_to_database
from app.database.queue.add_telegram_id_unique_constraint import add_telegram_id_unique_constraint


async def create_employees_table() -> bool:
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
                           first_level_manager BOOLEAN DEFAULT FALSE,
                           second_level_manager BOOLEAN DEFAULT FALSE,
                           rating INT DEFAULT 0,
                           is_in_antirating BOOLEAN DEFAULT FALSE,
                           has_one_rating_reset BOOLEAN DEFAULT FALSE,
                           was_a_good_fellow BOOLEAN DEFAULT FALSE
                           );
                           """)
        print("Employees table created successfully")

        add_constraint_result = await add_telegram_id_unique_constraint()

        if not add_constraint_result:
            return False

        return True
    except Exception as e:
        print(f"Error creating Employees table: {e}")
        return False
    finally:
        await close_connection(conn)