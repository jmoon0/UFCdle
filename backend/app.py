import traceback
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
    """Process only a few fighters at a time to avoid timeout"""
    try:
        data = request.get_json() or {}
        batch_size = data.get('batch_size', 3)  # Very small batch to avoid timeout
        start_index = data.get('start_index', 0)
        
        # Handle released fighters only on first batch
        if start_index == 0:
            released_fighters = scrape_released_fighters()
            for released_name in released_fighters:
                fighter = Fighter.query.filter_by(name=released_name).first()
                if fighter:
                    db.session.delete(fighter)
            db.session.commit()
            print(f"Removed {len(released_fighters)} released fighters")

        # Get scraped fighters
        fighters = scrape_fighter_roster()
        total_fighters = len(fighters)
        
        # Process only a small batch
        end_index = min(start_index + batch_size, total_fighters)
        batch_fighters = fighters[start_index:end_index]
        
        results = {
            "updated": 0,
            "added": 0,
            "skipped": 0,
            "errors": []
        }
        
        # Process each fighter in the batch
        for i, name in enumerate(batch_fighters):
            current_index = start_index + i
            print(f"Processing {current_index + 1}/{total_fighters}: {name}")
            
            try:
                details = get_fighter_details(name)
                if details:
                    existing_fighter = Fighter.query.filter_by(name=details['name']).first()
                    
                    if existing_fighter:
                        existing_fighter.wins = details["wins"]
                        existing_fighter.losses = details["losses"]
                        existing_fighter.weight_class = details["weightClass"]
                        existing_fighter.age = details["age"]
                        existing_fighter.bonus_stats = details["bonusStats"]
                        results["updated"] += 1
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
                        results["added"] += 1
                else:
                    results["skipped"] += 1
                    results["errors"].append(f"No details found for: {name}")
                    
            except Exception as e:
                results["skipped"] += 1
                results["errors"].append(f"Error with {name}: {str(e)}")
                print(f"Error processing {name}: {str(e)}")
        
        # Commit the batch
        db.session.commit()
        
        # Calculate progress
        progress = {
            "processed": end_index,
            "total": total_fighters,
            "percentage": round((end_index / total_fighters) * 100, 1),
            "has_more": end_index < total_fighters,
            "next_start": end_index if end_index < total_fighters else None
        }
        
        return jsonify({
            "success": True,
            "progress": progress,
            "results": results,
            "message": f"Processed fighters {start_index + 1}-{end_index} of {total_fighters}"
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/api/admin/db-progress", methods=["GET"])
def api_db_progress():
    """Check current database progress"""
    try:
        scraped_fighters = scrape_fighter_roster()
        db_fighters = Fighter.query.count()
        
        return jsonify({
            "database_count": db_fighters,
            "scraped_count": len(scraped_fighters),
            "completion_percentage": round((db_fighters / len(scraped_fighters)) * 100, 1) if scraped_fighters else 0
        })
        
    except Exception as e:
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

@app.route("/api/debug/single-fighter-detailed", methods=["POST"])
def debug_single_fighter_detailed():
    """Detailed debugging for a single fighter"""
    try:
        data = request.get_json() or {}
        fighter_name = data.get('name', 'Ilia Topuria')
        
        print(f"=== DEBUG: Testing fighter {fighter_name} ===")
        
        print("Testing fighter details...")
        details = get_fighter_details(fighter_name)
        
        if details:
            print(f"✅ Got details for {fighter_name}")
            print(f"Details: {details}")
            
            return jsonify({
                "success": True,
                "fighter_name": fighter_name,
                "got_details": True,
                "details": details
            })
        else:
            print(f"❌ Could not get details for {fighter_name}")
            return jsonify({
                "success": False,
                "fighter_name": fighter_name,
                "got_details": False,
                "error": "Could not get fighter details"
            })
        
    except Exception as e:
        print(f"Exception in debug route: {str(e)}")
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500
    

'''
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    
    #from scheduler import schedule_tasks
    #schedule_tasks(app, update_db)
    

    app.run(debug=True)
'''