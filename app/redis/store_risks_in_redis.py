import redis
import json

from typing import Literal

from app.database.queue.get_all_risks_levels_two_three_four import get_all_risks_levels_two_three_four


async def store_risks_in_redis() -> list[dict] | Literal[False] | None:
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
        risks = await get_all_risks_levels_two_three_four()

        if risks:
            # Convert the list of dictionaries (risk_data) to JSON and store it in Redis
            r.set('risk_levels_two_three_four', json.dumps(risks))
            print(f'Successfully stored risks in Redis: {risks}')
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