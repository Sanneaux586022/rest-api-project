import logging
import os
import models
from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from db import db, r

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint
logging.basicConfig(
    level=logging.INFO,
    format= "%(levelname)s - [%(name)s] %(message)s"
)

logger = logging.getLogger(__name__)
def create_app(db_url=None):

    app = Flask(__name__)

    # create a flask app 
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app) # inizializza l'estensione SQLAlchemy di Flask dandogli 
    #la nostra app flask in modo che possa connetter  l'app flask a sqlalchemy
    migrate = Migrate(app, db)
    import models
    api = Api(app)

    app.config["SECRET_KEY"] = "f22ba88eb2938478b75eb0a03360da31e5a7eb99585d5e3ff5470d8941170a11"
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        # return jwt_payload["jti"] in BLOCKLIST
        jti = jwt_payload["jti"]
        return r.get(jti) is not None
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token has been revoked.",
                    "error": "token_revoked"
                }
            ),
            401
        )
    
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required"
                }
            ),
            401
        )

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        # Look in the database and see whether the user is an admin!!
        if identity == 1:
            return {"is_admin": True}
        
        return {"is_admin": False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return(
            jsonify(
                {"message": "The token has expired.", "error": "token_expired"}
            ),
            401
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(jwt_header, jwt_payload):
        return(
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid token"}
            ),
            401
        )
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return(
            jsonify(
                {
                    "description": "Request does not contain an access token.", 
                    "error": "authtorization required."
                }
            ),
            401
        )
    
    
    # with app.app_context():
    #     db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app
# per utilizzare il docker-compose.debug.yml, fare: 
# docker compose -f docker-compose.yml -f docker-compose.debug.yml che farà? 
# utilizzerà qualunque servizio definito nel compose.yml ma poi sovrascriverà 
# alcuni servizi con a quelli definiti nel compose.debug.yml

# aggiornare i pacchetti con uv che usa pyproject.toml ed uv.lock--> uv sync
# docker run -dp 5005:5000 -w /app -v "$(pwd):/app" flask-smorest-api:latest
# openssl rand -hex 32
# f22ba88eb2938478b75eb0a03360da31e5a7eb99585d5e3ff5470d8941170a11
# prima fare partire redis collegandolo al netework sanonet che abbiamo creato docker run -d --name redis --network mynetwork redis:latest
# poi questo docker run -dp 5000:5000 -w /app -v "$(pwd):/app" --network sanonet -e REDIS_URL=redis://redis:6379 flask-smorest-api:latest 