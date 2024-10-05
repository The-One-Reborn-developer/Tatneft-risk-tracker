from app.database.queue.connect_to_database import connect_to_database
from app.database.queue.close_connection import close_connection
from app.database.queue.check_if_employee_exists import check_if_employee_exists


async def create_employee(employee) -> bool | None:
    """
    Create an employee in the database.

    Parameters
    ----------
    employee : dict
        A dictionary with the following keys:
            telegram_id : int
                The Telegram ID of the employee.
            chat_id : int
                The Telegram chat ID of the employee.
            telegram_username : str
                The Telegram username of the employee.
            full_name : str
                The full name of the employee.
            department : str
                The department of the employee.
            position : str
                The position of the employee.
            personnel_number : int
                The personnel number of the employee.
            manager_level : int
                The manager level of the employee.

    Returns
    -------
    bool
        True if the employee was added successfully, False if the employee already exists, None if an error occurred.
    """
    conn = None
    conn = await connect_to_database()
    try:
        employee_exists = await check_if_employee_exists(employee['telegram_id'])

        if employee_exists:
            return False

        await conn.execute(
            """
            INSERT INTO employees
            (telegram_id,
            chat_id,
            telegram_username,
            full_name,
            department,
            position,
            personnel_number,
            manager_level)
            VALUES
            ($1, $2, $3, $4, $5, $6, $7, $8)
            """,
            employee['telegram_id'],
            employee['chat_id'],
            employee['telegram_username'],
            employee['full_name'],
            employee['department'],
            employee['position'],
            employee['personnel_number'],
            employee['manager_level']
        )

        print(f'Employee {employee["telegram_id"]} added successfully.')
        return True
    except Exception as e:
        print(f"Error adding employee: {e}")
        return None
    finally:
        if conn:
            await close_connection(conn)