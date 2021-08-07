from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from pathlib import Path

from app.main.config import get_config, Config
from app.main.log import logger, get_handler


db = SQLAlchemy()
# bcrypt = Bcrypt()

jwt = JWTManager()


def create_app(config_name):
    # logname = Config.LOG_FILE
    # log_name = Path(r"C:\Users\Roy\Documents\GitHub\MyGit_folder\Projects\Send_IP_for_me", "logs", "server.log")
    log_name = Path(Path.cwd(), "logs", "server.log")
    logger.addHandler(get_handler(log_name))
    app = Flask(__name__)
    app.config.from_object(get_config(config_name))
    db.init_app(app)
    # bcrypt.init_app(app)
    jwt.init_app(app)
    return app
