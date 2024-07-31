from models import Fighter, DailySolution
from datetime import date, datetime
from pytz import timezone
import random
import re
from config import db

#Selects a random fighter and bonus stat from the database as the daily solution and stores it in the dailysolution table
def select_daily_fighter():
    eastern = timezone("US/Eastern")
    today = datetime.now(eastern).date()

    existing_selection = DailySolution.query.filter_by(date=today).first()
    if existing_selection:
         return existing_selection
    
    fighters = Fighter.query.all()

    if not fighters:
         print("Error: fighters not found.")
         return None
    
    bonus_stats = ["winsByKo", "winsBySub", "sigStrikesAccuracy", "sigStrikesDefense", "takedownDefense"]
    selected_bonus_stat = random.choice(bonus_stats)

    selected_fighter = random.choice(fighters)
    daily_solution = DailySolution(date=today, fighter_id=selected_fighter.id, bonus_stat=selected_bonus_stat)
    db.session.add(daily_solution)
    db.session.commit()
    print("Daily fighter updated.")

    return daily_solution

#Retrieves the current daily solution fighter
def get_daily_fighter():
    eastern = timezone("US/Eastern")
    today = datetime.now(eastern).date()
    daily_solution = DailySolution.query.filter_by(date=today).first()

    #If the daily solution does not exist, calls select_daily_fighter to store a new daily solution
    if daily_solution:
         return daily_solution
    else:
         return select_daily_fighter()

def compare_stat(stat1, stat2, limit):
    stat1 = int(stat1)
    stat2 = int(stat2)

    if stat1 == stat2:
            return "correct"

    #Lower means stat should have an arrow up and vice versa
    elif abs(stat1 - stat2) < limit:
        return "close higher" if stat1 < stat2 else "close lower"
    
    else:
        return "incorrect higher" if stat1 < stat2 else "incorrect lower"
    
        
def parse_height(height):
    match = re.match(r"(\d+)'(\d+)\"", height)
    if not match:
        raise ValueError(f"Invalid height format: {height}")
    
    feet = int(match.group(1))
    inches = int(match.group(2))
    total_inches = feet * 12 + inches

    return total_inches

def compare_weight_classes(guess, solution):
    weights = {
        "flyweight": 0,
        "bantamweight": 1,
        "featherweight": 2,
        "lightweight": 3,
        "welterweight": 4,
        "middleweight": 5,
        "light heavyweight": 6,
        "heavyweight": 7,

        #"women's strawweight": 15,
        #"women's flyweight": 16,
        #"women's bantamweight": 17,
        #"women's featherweight": 18,
    }
    guess_val = weights[str(getattr(guess, "weight_class")).lower()]
    solution_val = weights[str(getattr(solution, "weight_class")).lower()]

    return compare_stat(guess_val, solution_val, 2)

def compare_heights(guess, solution):
    guess_val = parse_height(getattr(guess, "height"))
    solution_val = parse_height(getattr(solution, "height"))

    return compare_stat(guess_val, solution_val, 4)

def compare_bonus_stats(guess, solution, bonus_stat):
    guess_bonus_val = int(guess.bonus_stats.get(bonus_stat))
    solution_bonus_val = int(solution.bonus_stats.get(bonus_stat))

    if guess_bonus_val:
        return compare_stat(guess_bonus_val, solution_bonus_val, 5)
    else:
        return "X"

def compare_fighters(guess, solution, bonus_stat):
    comparison = {}

    comparison["guess"] = guess.to_json()

    for attr in ["wins", "losses", "age",]:
        guess_val = getattr(guess, attr)
        solution_val = getattr(solution, attr)

        comparison[attr] = compare_stat(guess_val, solution_val, 4)
    
    comparison["weightClass"] = compare_weight_classes(guess, solution)
    comparison["height"] = compare_heights(guess, solution)
    comparison["bonus_stat"] = compare_bonus_stats(guess, solution, bonus_stat)

    if(getattr(guess, "name") == getattr(solution, "name")):
        comparison["name"] = "correct"
    else:
        comparison["name"] = "none"

    return comparison

