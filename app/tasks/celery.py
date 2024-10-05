import celery
import asyncio

app = celery.Celery('tasks', broker='redis://localhost:6379/0')

# Optional: Configure Celery settings
app.conf.update(
    task_routes={
        'app.tasks.database_tasks.*': {'queue': 'database_tasks_queue'}
    }
)

app.conf.broker_connection_retry_on_startup = True


@app.task
def create_employees_table_task() -> bool | None:
    """
    Creates the employees table in the PostgreSQL database.

    Returns True if the table was created successfully, False otherwise, or None if an error occurred.
    """
    from app.database.models.create_employees_table import create_employees_table
    return asyncio.run(create_employees_table())


@app.task
def create_risks_table_task() -> bool | None:
    """
    Creates the risks table in the PostgreSQL database.

    Returns True if the table was created successfully, None if an error occurred.
    """
    from app.database.models.create_risks_table import create_risks_table
    return asyncio.run(create_risks_table())


@app.task
def get_employees_rating_task() -> list | None:
    """
    Get a list of employees with their names, departments, positions and ratings,
    sorted in descending order of rating.

    Returns:
        list | None: A list of dictionaries, each dictionary containing the full name,
            department, position and rating of an employee. If an error occurs,
            returns None.
    """
    from app.database.queue.get_employees_rating import get_employees_rating
    return asyncio.run(get_employees_rating())


@app.task
def get_all_level_one_managers_task() -> list | None:
    """
    Get a list of all chat IDs of level one managers.

    Returns a list of all chat IDs of level one managers if successful, None if an error occurred.
    """
    from app.database.queue.get_all_level_one_managers import get_all_level_one_managers
    return asyncio.run(get_all_level_one_managers())


@app.task
def get_all_level_two_managers_task() -> list | None:
    """
    Get a list of all chat IDs of level two managers.

    Returns a list of all chat IDs of level two managers if successful, None if an error occurred.
    """
    from app.database.queue.get_all_level_two_managers import get_all_level_two_managers
    return asyncio.run(get_all_level_two_managers())


@app.task
def get_all_level_three_managers_task() -> list | None:
    """
    Get a list of all chat IDs of level three managers.

    Returns a list of all chat IDs of level three managers if successful, None if an error occurred.
    """
    from app.database.queue.get_all_level_three_managers import get_all_level_three_managers
    return asyncio.run(get_all_level_three_managers())


@app.task
def create_employee_task(employee) -> bool | None:
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
        True if the employee was added successfully, None if an error occurred.
    """
    from app.database.queue.create_employee import create_employee
    return asyncio.run(create_employee(employee))


@app.task
def create_risk_task(risk) -> bool | None:
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
    from app.database.queue.create_risk import create_risk
    return asyncio.run(create_risk(risk))


@app.task
def get_all_risks_levels_two_three_four_task() -> list | None:
    """
    Get a list of all request_number of risks of level two, three and four.

    Returns a list of all request_number of risks of level two, three and four if successful, None if an error occurred.
    """
    from app.database.queue.get_all_risks_levels_two_three_four import get_all_risks_levels_two_three_four
    return asyncio.run(get_all_risks_levels_two_three_four())