from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import os.path
from flask_bcrypt import Bcrypt
from flask_login import LoginManager



app = Flask(__name__)
if os.path.exists('/mnt/c/Users/drewc/OneDrive/Documents/GitHub/rh-web/rh.db'):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/c/Users/drewc/OneDrive/Documents/GitHub/rh-web/rh.db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/drewxcom/rh.db'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from flask_app.main.routes import main
from flask_app.manage.routes import manage

app.register_blueprint(main)
app.register_blueprint(manage)

