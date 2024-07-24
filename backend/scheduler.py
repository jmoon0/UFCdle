from utils import select_daily_fighter
from apscheduler.schedulers.background import BackgroundScheduler

#Pass update_db as argument to avoid circular import D: 
def schedule_tasks(app, update_db):
    scheduler = BackgroundScheduler(timezone="US/Eastern")

    def select_daily_fighter_with_context():
        with app.app_context():
            select_daily_fighter()

    def update_db_with_context():
        with app.app_context():
            update_db()

    # Daily fighter selection at 12am EST 
    scheduler.add_job(select_daily_fighter_with_context, 'cron', hour=0, minute=0)

    # Weekly database update at 12am EST Monday
    scheduler.add_job(update_db_with_context, 'cron', day_of_week="sun", hour=10, minute=0)

    scheduler.start()