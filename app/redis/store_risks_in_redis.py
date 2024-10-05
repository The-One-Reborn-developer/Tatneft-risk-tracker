import redis
import json

from typing import Literal

from app.tasks.celery import get_all_risks_levels_two_three_four_task


def store_risks_in_redis() -> list[dict] | Literal[False] | None:
    """
    Store risks of level two, three and four in Redis.

    This function first activates a Celery task to fetch the risks of level two, three and four.
    It then waits for the task to complete and gets the result.
    If the result is not None, it converts the list of dictionaries (risk_data) to JSON and stores it in Redis under the key 'risk_levels_two_three_four'.
    If no risks of level two, three and four were found, it returns False.
    If an error occurs, it returns None.
    """
    r = redis.Redis(host='localhost', port=6379, db=0)
    
    # Activate the task to fetch the risks
    try:
        risks = get_all_risks_levels_two_three_four_task.delay()

        # Wait for the task to complete and get the result
        risks_data = risks.get(timeout=10)  # Adjust timeout if necessary

        if risks_data:
            # Convert the list of dictionaries (risk_data) to JSON and store it in Redis
            r.set('risk_levels_two_three_four', json.dumps(risks_data))
            print(f'Successfully stored risks in Redis: {risks_data}')
            return True
        else:
            print("No risks of level two, three and four found")
            return False
    except Exception as e:
        print(f"Error storing risks in Redis: {e}")
        return None
    finally:
        # Close the Redis connection (optional)
        r.close()