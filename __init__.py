from datetime import timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from .api import check_active
from flask import Flask, sessions
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import Flask, session
from flask_sslify import SSLify
"""
    Getting the latest config
"""
import configparser
config = configparser.ConfigParser()
import os
script_dir = os.path.dirname(__file__)
with open(os.path.join(script_dir, './.data/server.cfg'), 'r') as f:
    config.read_file(f)

config_state = "DEFAULT" if config.get("DEFAULT","debug")!="yes" else "DEBUG"
"""
    Scheduling the remove task
"""
cron = BackgroundScheduler(daemon=True)
cron.start()
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('iot.log')
c_handler.setLevel(logging.WARNING)
f_handler.setLevel(logging.ERROR)

@cron.scheduled_job('interval', seconds=int(config.get(config_state,"time_out")))
def check():
    check_active()


atexit.register(lambda: cron.shutdown(wait=False))

db = SQLAlchemy()
from .models import User, client_entry

def create_app():
    app = Flask(__name__)
    #app.permanent_session_lifetime = timedelta(minutes=int(config.get(config_state,"session_lifetime")))
    app.config['SECRET_KEY'] = config.get(config_state,"server_secret_key")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .backend_api import backend_api as bapi
    app.register_blueprint(bapi)


    @app.before_first_request
    def create_tables():
        db.create_all()

    return app

