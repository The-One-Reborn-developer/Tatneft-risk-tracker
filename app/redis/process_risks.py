import redis
import json

from typing import Literal

async def process_risks() -> bool | None:
    # Initialize Redis connection
    r = redis.Redis(host='localhost', port=6379, db=0)
    
    try:
        # Get the stored risks from Redis
        risks_data = r.get('risk_levels_two_three_four')

        if risks_data:
            risks = json.loads(risks_data)  # Convert the JSON back to a Python list of dictionaries
            
            for risk in risks:
                request_number = risk.get('request_number')
                risk_level = risk.get('risk_level')
                claimant_telegram_id = risk.get('claimant_telegram_id')
                performer_telegram_id = risk.get('performer_telegram_id')
                
                # Perform different actions based on the risk_level
                if risk_level == 2:
                    process_level_two_risk(request_number, claimant_telegram_id, performer_telegram_id)
                elif risk_level == 3:
                    process_level_three_risk(request_number, claimant_telegram_id, performer_telegram_id)
                elif risk_level == 4:
                    process_level_four_risk(request_number, claimant_telegram_id, performer_telegram_id)
                else:
                    print(f"Unknown risk level {risk_level} for request {request_number} from {claimant_telegram_id} to {performer_telegram_id}")
        
            print("Successfully processed risks from Redis")
            return True
        else:
            print("No risks found in Redis")
            return False
    except Exception as e:
        print(f"Error processing risks from Redis: {e}")
        return None
    finally:
        # Close the Redis connection (optional)
        r.close()

def process_level_two_risk(request_number, claimant_telegram_id, performer_telegram_id) -> Literal[True] | None:
    print(f"Processing level 2 risk: {request_number} from {claimant_telegram_id} to {performer_telegram_id}")
    # Add your logic here
    return True

def process_level_three_risk(request_number, claimant_telegram_id, performer_telegram_id) -> Literal[True] | None:
    print(f"Processing level 3 risk: {request_number} from {claimant_telegram_id} to {performer_telegram_id}")
    # Add your logic here
    return True

def process_level_four_risk(request_number, claimant_telegram_id, performer_telegram_id) -> Literal[True] | None:
    print(f"Processing level 4 risk: {request_number}, from {claimant_telegram_id} to {performer_telegram_id}")
    # Add your logic here
    return True
