from db import db

# Game data model to store in database
class GameModel(db.Model):
    __tablename__ = "games"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    name = db.Column(db.String(80))
    user_score = db.Column(db.Integer)
    opponent_score = db.Column(db.Integer)

    # Initialize game model
    def __init__(self, user_id, name, user_score, opponent_score):
        self.user_id = user_id
        self.name = name
        self.user_score = user_score
        self.opponent_score = opponent_score

    # Return the json formatted game
    def json(self):
        return {
            "name": self.name,
            "user_score": self.user_score,
            "opponent_score": self.opponent_score
        }

    # Find all games in the database by user id
    @classmethod
    def find_all_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    # Find a game in the database by id
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    # Save game to database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # Delete game from database
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
