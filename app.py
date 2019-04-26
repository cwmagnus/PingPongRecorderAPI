import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from db import db
from blacklist import BLACKLIST

# Configure application and database
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["DEBUG"] = os.environ.get("DEBUG_APP", True)
api = Api(app)

# Configure jwt
app.config["JWT_SECRET_KEY"] = os.urandom(20)
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]
jwt = JWTManager(app)

# Checks if the jwt is in the blacklist
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST

# Check if the token is expired
@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        "message": "The token has expired.",
        "error": "token_expired"
    }), 401

# Check if the token is invalid
@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        "message": "Signature verification failed.",
        "error": "invalid_token"
    }), 401

# Check if the request has a token
@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "description": "Request does not contain an access token.",
        "error": "authorization_required"
    }), 401

# Check if the token needs refreshed
@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        "description": "The token is not fresh.",
        "error": "fresh_token_required"
    }), 401

# Revoke a token
@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        "description": "The token has been revoked.",
        "error": "token_revoked"
    }), 401

# Create the database tables
@app.before_first_request
def create_tables():
    db.create_all()

# TODO: Register endpoints

# Run the api
if __name__ == "__main__":
    from db import db
    db.init_app(app)

    if app.config["DEBUG"]:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(port=5000)