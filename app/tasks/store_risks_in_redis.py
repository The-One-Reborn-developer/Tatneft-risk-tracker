from app.tasks.celery import get_all_risks_levels_two_three_four_task
import redis

# Initialize Redis connection
r = redis.Redis(host='localhost', port=6379, db=0)

def store_risks_in_redis():
    # Activate the task to fetch the risks
    risks = get_all_risks_levels_two_three_four_task.delay()

    # Wait for the task to complete and get the result
    request_numbers = risks.get(timeout=10)  # Adjust timeout if necessary

    if request_numbers:
        # Store the list of risks in Redis
        r.set('risk_levels_two_three_four', str(request_numbers))
        print(f'Successfully stored risks in Redis: {request_numbers}')
    else:
        print("No risks found or error occurred")