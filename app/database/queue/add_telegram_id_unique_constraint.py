from app.database.queue.close_connection import close_connection
from app.database.queue.connect_to_database import connect_to_database


async def add_telegram_id_unique_constraint() -> bool:
    conn = await connect_to_database()
    try:
        # Execute the SQL command to add a unique constraint
        await conn.execute("""
            ALTER TABLE employees ADD CONSTRAINT unique_telegram_id UNIQUE (telegram_id);
        """)
        print("Unique constraint on telegram_id added successfully.")
        return True
    except Exception as e:
        print(f"Error adding unique constraint: {e}")
        return False
    finally:
        await close_connection(conn)