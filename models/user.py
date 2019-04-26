from db import db

# User data model to store in database
class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    wins = db.Column(db.Integer)
    losses = db.Column(db.Integer)

    # Initialize user model
    def __init__(self, username, password):
        self.username = username
        self.password = password

    # Return the json formatted user
    def json(self):
        return {
            "id": self.id,
            'username': self.username
        }

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    # Find user in the database by id
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    # Save user to database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # Delete user from database
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
