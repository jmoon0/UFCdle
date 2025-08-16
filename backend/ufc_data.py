import traceback
from ufc import get_fighter
import time
import random

def to_int(value):
    try:
        float_value = float(value)
        if float_value.is_integer():
            return int(float_value)
        return int(float_value * 100)
    except ValueError:
        return value

def to_percentage(part, whole):
    dividend = to_int(part)
    divisor = to_int(whole)
    if dividend == 0 or divisor == 0:
        return 0
    percentage = dividend / divisor
    return (to_int(percentage))

def get_fighter_details(name, max_retries=3):
    
    # Handle special cases
    if name.lower() == "ian machado garry":
        name = "ian garry"
    
    for attempt in range(max_retries):
        try:
            # Add random delay to avoid rate limiting
            if attempt > 0:
                delay = random.uniform(2, 5) * (attempt + 1)
                print(f"Retrying {name} in {delay:.1f} seconds...")
                time.sleep(delay)
            
            fighter = get_fighter(name)
            if fighter:
                return {
                    "name": fighter["name"],
                    "wins": fighter["wins"]["total"],
                    "losses": fighter["losses"]["total"],
                    "weightClass": fighter["weight_class"],
                    "age": fighter["age"],
                    "height": fighter["height"],
                    "bonusStats": {
                        "winsByKo": to_percentage(fighter["wins"]["ko/tko"], fighter["wins"]["total"]),
                        "winsBySub": to_percentage(fighter["wins"]["submissions"], fighter["wins"]["total"]),
                        "sigStrikesAccuracy": to_percentage(fighter["strikes"]["landed"], fighter["strikes"]["attempted"]),
                        "sigStrikesDefense": to_int(fighter["strikes"]["striking defense"]),
                        "takedownDefense": to_int(fighter["takedowns"]["takedown defense"]),
                    }
                }
        except Exception as e:
            error_msg = str(e).lower()
            print(f"Attempt {attempt + 1} failed for {name}: {str(e)}")
            
            # If it's a "not found" error and we've tried multiple times, skip
            if "not found" in error_msg and attempt == max_retries - 1:
                print(f"Skipping {name} - consistently not found")
                return None
            
            # If it's a rate limit or connection error, wait longer
            if any(keyword in error_msg for keyword in ['rate', 'blocked', 'connection', 'timeout']):
                if attempt < max_retries - 1:
                    wait_time = random.uniform(5, 10) * (attempt + 1)
                    print(f"Rate limited. Waiting {wait_time:.1f} seconds...")
                    time.sleep(wait_time)
                    continue
    
    print(f"Failed to get details for {name} after {max_retries} attempts")
    traceback.print_exc()
    return None