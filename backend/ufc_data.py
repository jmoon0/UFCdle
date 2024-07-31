from ufc import get_fighter

#Helper function to convert to int due to inconsistencies with UFC package
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

def get_fighter_details(name):
    #Sherdog won't show Ian Garry's profile if it has Machado in it for some reason
    if name.lower() == "ian machado garry":
        name = "ian garry"

    try:
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
    except BaseException as e:
        print(f"Error getting details for {name}: {str(e)}")
    
    return None