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
                    name=details["name"], # type: ignore
                    wins=details["wins"], # type: ignore
                    losses=details["losses"], # type: ignore
                    weight_class=details["weightClass"], # type: ignore
                    age=details["age"], # type: ignore
                    height=details["height"], # type: ignore
                    bonus_stats=details["bonusStats"], # type: ignore
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
    bonus_stat = DailySolution.query.filter_by(date=today).first().bonus_stat # type: ignore

    for fighter in random.sample(fighters, sample_size):
        bs = fighter.bonus_stats.get(bonus_stat, "N/A") if fighter.bonus_stats else "N/A"
        print(f"Name: {fighter.name}, Wins: {fighter.wins}, Losses: {fighter.losses}, Weight Class: {fighter.weight_class} Bonus Stat ({bonus_stat}): {bs}")

@app.cli.command("check-fighter")
@click.argument("name")
def check_fighter(name):
    fighter = Fighter.query.filter_by(name=name).first()
    if fighter:
        click.echo(f"Fighter details: {fighter.to_json()}")
    else:
        click.echo(f"Fighter {name} not found.")

# Routes to replace CLI commands (since cant use in vercel)

@app.route("/api/admin/update-db", methods=["POST"])
def api_update_db():
    """Replace the CLI update-db command"""
    try:
        released_fighters = scrape_released_fighters()
        for released_name in released_fighters:
            fighter = Fighter.query.filter_by(name=released_name).first()
            if fighter:
                db.session.delete(fighter)

        fighters = scrape_fighter_roster()
        updated_count = 0
        added_count = 0
        
        for name in fighters:
            details = get_fighter_details(name)
            if details:
                existing_fighter = Fighter.query.filter_by(name=details['name']).first()
                
                if existing_fighter:
                    existing_fighter.wins = details["wins"]
                    existing_fighter.losses = details["losses"]
                    existing_fighter.weight_class = details["weightClass"]
                    existing_fighter.age = details["age"]
                    existing_fighter.bonus_stats = details["bonusStats"]
                    updated_count += 1
                else:
                    new_fighter = Fighter(
                        name=details["name"],  # type: ignore
                        wins=details["wins"],  # type: ignore
                        losses=details["losses"],  # type: ignore
                        weight_class=details["weightClass"],  # type: ignore
                        age=details["age"],  # type: ignore
                        height=details["height"],  # type: ignore
                        bonus_stats=details["bonusStats"],  # type: ignore
                    )
                    db.session.add(new_fighter)
                    added_count += 1
        
        db.session.commit()
        return jsonify({
            "success": True, 
            "updated": updated_count, 
            "added": added_count
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/api/admin/init-db", methods=["POST"])
def api_init_db():
    """Initialize database tables"""
    try:
        db.create_all()
        return jsonify({"success": True, "message": "Database initialized"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/admin/db-stats", methods=["GET"])
def api_db_stats():
    """Get database statistics"""
    try:
        fighter_count = Fighter.query.count()
        solution_count = DailySolution.query.count()
        
        return jsonify({
            "fighters": fighter_count,
            "solutions": solution_count,
            "scraped_count": len(scrape_fighter_roster())
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/admin/select-daily", methods=["POST"])
def api_select_daily():
    """Manually trigger daily fighter selection"""
    try:
        from utils import select_daily_fighter
        daily_solution = select_daily_fighter()
        
        if daily_solution:
            return jsonify({
                "success": True,
                "fighter": daily_solution.fighter.name,
                "bonus_stat": daily_solution.bonus_stat
            })
        else:
            return jsonify({"error": "Failed to select daily fighter"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
    return jsonify(fighter.to_json())            # type: ignore

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
    guess_name = data.get('name') # type: ignore

    fighter = Fighter.query.filter_by(name=guess_name).first()
    if not fighter:
        print("Fighter not found:", guess_name) 
        return jsonify({'error': 'Fighter not found.'}), 404
    
    daily_solution = get_daily_fighter()

    if not daily_solution:
        return jsonify({'error': 'No daily fighter selected.'}), 404
    
    daily_fighter = daily_solution.fighter
    bonus_stat = daily_fighter.bonus_stat

    comparison = compare_fighters(fighter, daily_fighter, bonus_stat)

    return jsonify(comparison), 200

'''
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    
    #from scheduler import schedule_tasks
    #schedule_tasks(app, update_db)
    

    app.run(debug=True)
'''