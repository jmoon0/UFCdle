from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.mutable import MutableDict
from config import db

class Fighter(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False, unique = True)
    wins = db.Column(db.Integer, nullable = False)
    losses = db.Column(db.Integer, nullable = False)
    weight_class = db.Column(db.String(25), nullable = False)
    age = db.Column(db.Integer, nullable = False)
    height = db.Column(db.String(8), nullable = False)

    # New JSON field for bonus stats
    bonus_stats = db.Column(MutableDict.as_mutable(JSON), nullable=True, default=dict)
    
    def to_json(self):
        return{
            "id": self.id,
            "name": self.name,
            "wins": self.wins,
            "losses": self.losses,
            "weightClass": self.weight_class,
            "age": self.age,
            "height": self.height,
            "bonusStats": self.bonus_stats,
        }
    
class DailySolution(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.Date, unique = True, nullable = False)
    fighter_id = db.Column(db.Integer, db.ForeignKey('fighter.id'),nullable = False)
    fighter = db.relationship('Fighter', backref=db.backref('daily_selections', lazy=True))
    bonus_stat = db.Column(db.String(50), nullable=False)

    def to_json(self):
        return{
            "id": self.id,
            "date": self.date.isoformat(),
            "fighterId": self.fighter_id,
            "fighter": self.fighter.to_json(),
            "bonusStat": self.bonus_stat or {},
        }