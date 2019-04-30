from flask_restful import Resource, reqparse
from flask_jwt_extended import *
from models.game import GameModel
from models.user import UserModel

# Record a game
class GameRecord(Resource):
    # Set up parser
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name",
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument(
        "user_score",
        type = int,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument(
        "opponent_score",
        type = int,
        required = True,
        help = "This field cannot be left blank!"
    )

    @jwt_required
    def post(self):
        data = self.parser.parse_args()
        user_id = get_jwt_identity()

        game = GameModel(user_id, data["name"], data["user_score"], data["opponent_score"])
        user = UserModel.find_by_id(user_id)
        
        if game.user_score > game.opponent_score:
            user.wins += 1
        else:
            user.losses += 1

        user.save_to_db()
            
        try:
            game.save_to_db()
        except:
            return {"message": "An error occurred while recording this game."}, 500

        return {"message": "Game recorded successfully."}, 201

# Get a game by id
class GameGet(Resource):
    @jwt_required
    def get(self, _id):
        game = GameModel.find_by_id(_id)

        if game:
            return game.json()

        return {"message": "Item not found."}, 404

# Get all recorded games
class GameList(Resource):
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        games = [game.json() for game in GameModel.find_all_by_user_id(user_id)]
        
        if games:
            return {"games": games}, 200

        return {"message": "No games were found."}, 404 

