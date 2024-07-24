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

def get_fighter_details(name):
    
    #Sherdog won't show Garry's profile if it has Machado in it for some reason
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
                    "sigStrikesLanded": to_int(fighter["strikes"]["landed"]),
                    "sigStrikesAttempted": to_int(fighter["strikes"]["attempted"]),
                    "takedownsLanded": to_int(fighter["takedowns"]["landed"]),
                    "takedownsAttempted": to_int(fighter["takedowns"]["attempted"]),
                    "sigStrikesDefense": to_int(fighter["strikes"]["striking defense"]),
                    "takedownDefense": to_int(fighter["takedowns"]["takedown defense"]),
                }
            }
    except BaseException as e:
        print(f"Error getting details for {name}: {str(e)}")
    
    return None