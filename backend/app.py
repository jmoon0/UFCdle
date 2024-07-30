import click
from flask import request, jsonify
from models import Fighter, DailySolution
from config import app, db
from scraper import scrape_fighter_roster, scrape_released_fighters
from ufc_data import get_fighter_details
from utils import get_daily_fighter, compare_fighters
from pytz import timezone
from datetime import datetime

'''
@app.cli.command("reset-db")
def reset_db():
    db.drop_all()
    db.create_all()
    print("Reset complete.")
'''

@app.cli.command("update-db")
def update_db():
    released_fighters = scrape_released_fighters()
    for released_name in released_fighters:
        fighter = Fighter.query.filter_by(name=released_name).first()
        if fighter:
            db.session.delete(fighter)

    fighters = scrape_fighter_roster()
    for name in fighters:
        details = get_fighter_details(name)
        if details:
            #Names in the database are not the same as the ones in the scraped wiki tables
            #Checks if a fighter already exists in the db
            existing_fighter = Fighter.query.filter_by(name=details['name']).first()

            #Update existing fighter stats
            if existing_fighter:
                existing_fighter.wins = details["wins"]
                existing_fighter.losses = details["losses"]
                existing_fighter.weight_class = details["weightClass"]
                existing_fighter.age = details["age"]
                existing_fighter.bonus_stats = details["bonusStats"]
            #Add new fighter
            else:
                new_fighter = Fighter(
                    name=details["name"], 
                    wins=details["wins"], 
                    losses=details["losses"], 
                    weight_class=details["weightClass"], 
                    age=details["age"], 
                    height=details["height"],
                    bonus_stats=details["bonusStats"],
                    )
                db.session.add(new_fighter)
        
    print("Db update finished.")
    db.session.commit()

@app.cli.command("update-fighter")
@click.argument("name")
def update_fighter(name):
    details = get_fighter_details(name)
    if details:
        existing_fighter = Fighter.query.filter_by(name=details['name']).first()

        if existing_fighter:
            existing_fighter.wins = details["wins"]
            existing_fighter.losses = details["losses"]
            existing_fighter.weight_class = details["weightClass"]
            existing_fighter.age = details["age"]
            existing_fighter.bonus_stats = details["bonusStats"]
            
            click.echo(f"Updated stats for: {name}")
            db.session.commit()
        else:
            click.echo(f"Fighter {name} not found in the database. No update was made.")
    else:
        click.echo(f"Details for fighter {name} could not be retrieved.")

@app.cli.command("check-db")
def check_db():
    print(f"Scraped fighter list length: {len(scrape_fighter_roster())}")

    fighters = Fighter.query.all()
    print(f"Total fighters in database: {len(fighters)}")
    
    # Check a few random fighters
    import random
    sample_size = min(10, len(fighters))

    eastern = timezone("US/Eastern")
    today = datetime.now(eastern).date()
    bonus_stat = DailySolution.query.filter_by(date=today).first().bonus_stat

    for fighter in random.sample(fighters, sample_size):
        bs = fighter.bonus_stats.get(bonus_stat, "N/A") if fighter.bonus_stats else "N/A"
        print(f"Name: {fighter.name}, Wins: {fighter.wins}, Losses: {fighter.losses}, Weight Class: {fighter.weight_class} Bonus Stat ({bonus_stat}): {bs}")

@app.cli.command("check-fighter")
@click.argument("name")
def check_db(name):
    fighter = Fighter.query.filter_by(name=name).first()
    if fighter:
        click.echo(f"Fighter details: {fighter.to_json()}")
    else:
        click.echo(f"Fighter {name} not found.")

@app.route("/api/fighters", methods=["GET"])
def get_fighters():
    fighters = Fighter.query.all()
    json_fighters = list(map(lambda x: x.to_json(), fighters))
    return jsonify({"fighters": json_fighters})

@app.route("/api/past-solutions", methods=["GET"])
def get_past_solutions():
    solutions = DailySolution.query.all()
    json_solutions = list(map(lambda x: x.to_json(), solutions))
    return jsonify({"pastSolutions": json_solutions})

@app.route("/api/daily-fighter", methods=["GET"])
def daily_fighter(): 
    fighter = get_daily_fighter()
    return jsonify(fighter.to_json())           

@app.route("/api/search", methods=["GET"])
def search():
    query = request.args.get("q",)
    if query:
        fighters = Fighter.query.filter(Fighter.name.ilike(f"%{query}%")).limit(20).all()
        return jsonify([fighter.name for fighter in fighters])
    
    return jsonify([])

@app.route("/api/guess", methods=["POST"])
def guess():
    data = request.json
    guess_name = data.get('name')

    fighter = Fighter.query.filter_by(name=guess_name).first()
    if not fighter:
        print("Fighter not found:", guess_name) 
        return jsonify({'error': 'Fighter not found.'}), 404
    
    daily_fighter = get_daily_fighter().fighter
    bonus_stat = get_daily_fighter().bonus_stat

    comparison = compare_fighters(fighter, daily_fighter, bonus_stat)

    return jsonify(comparison), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    '''
    from scheduler import schedule_tasks
    #schedule_tasks(app, update_db)
    '''

    app.run(debug=True)