from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail, Message
from flask_sitemap import Sitemap
from os import path, remove
import calendar
import pytz


# Globally accessible libraries
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()
ext =Sitemap()
root = path.dirname(path.abspath(__file__))

def create_app():
    ''' Initialize the core application'''
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    # Initialize Plugings
    db.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)
    ext.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'main_bp.login'
    login_manager.login_message_category = 'info'

    with app.app_context():
        # Register Blueprints
        from . main import main_bp
        from . manage import manage_bp
        from . errors import handlers

        app.register_blueprint(main_bp.main)
        app.register_blueprint(manage_bp.manage)
        app.register_blueprint(handlers.errors)

        return app
