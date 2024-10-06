import asyncio
import celery

from celery.schedules import crontab
from typing import Literal

app = celery.Celery('tasks', broker='redis://localhost:6379/0')

# Optional: Configure Celery settings
app.conf.update(
    task_routes={
        'app.tasks.database_tasks.*': {'queue': 'database_tasks_queue'}
    },
    broker_connection_retry_on_startup=True,
    result_backend='redis://localhost:6379/0',
    beat_schedule={
        'store_risks_task': {
            'task': 'app.tasks.celery.store_risks_task',
            'schedule': crontab(minute=0, hour=8),
        },
        'process_risks_task': {
            'task': 'app.tasks.celery.process_risks_task',
            'schedule': crontab(minute=30, hour=8),
        }
    },
    timezone='Europe/Moscow'
)


@app.task
def create_employees_table_task() -> bool | None:
    """
    Creates the employees table in the PostgreSQL database.

    Returns True if the table was created successfully, False otherwise, or None if an error occurred.
    """
    from app.database.models.create_employees_table import create_employees_table
    return asyncio.run(create_employees_table())


@app.task
def create_risks_table_task() -> Literal[True] | None:
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
        True if the employee was added successfully, False if the employee already exists, None if an error occurred.
    """
    from app.database.queue.create_employee import create_employee
    return asyncio.run(create_employee(employee))


@app.task
def update_employee_task(telegram_id, **kwargs) -> Literal[True] | None:
    """
    Update an employee in the database.

    Parameters
    ----------
    telegram_id : int
        The Telegram ID of the employee to update.
    kwargs : dict
        A dictionary containing the fields to update and their new values.

    Returns
    -------
    bool
        True if the employee was updated successfully, None if an error occurred.
    """
    from app.database.queue.update_employee import update_employee
    return asyncio.run(update_employee(telegram_id, **kwargs))


@app.task
def create_risk_task(risk) -> Literal[True] | None:
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
def store_risks_task() -> list[dict] | Literal[False] | None:
    """
    Store risks of level two, three and four in Redis.

    This function first activates a Celery task to fetch the risks of level two, three and four.
    It then waits for the task to complete and gets the result.
    If the result is not None, it converts the list of dictionaries (risk_data) to JSON and stores it in Redis under the key 'risk_levels_two_three_four'.
    If no risks of level two, three and four were found, it returns False.
    If an error occurs, it returns None.
    """
    from app.redis.store_risks import store_risks
    return asyncio.run(store_risks())


@app.task
def process_risks_task() -> bool | None:
    """
    Process risks in Redis.

    This function first activates a Celery task to process risks in Redis.
    It then waits for the task to complete and gets the result.
    If the result is not None, it returns True.
    If an error occurs, it returns None.
    """
    from app.redis.process_risks import process_risks
    return asyncio.run(process_risks())