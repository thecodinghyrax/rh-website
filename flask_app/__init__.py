from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import os.path
from flask_bcrypt import Bcrypt
from flask_login import LoginManager



app = Flask(__name__)
# Desktop 
if os.path.exists('/mnt/c/Users/drewc/OneDrive/Documents/GitHub/rh-web/rh.db'):
    print("!!!!!!!! I'm using the local desktop db path")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/c/Users/drewc/OneDrive/Documents/GitHub/rh-web/rh.db'
    
# Laptop
elif os.path.exists('/mnt/c/Users/drewc/GitHub/rh-website'):
    print("!!!!!!!! I'm using the local laptop db path")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/c/Users/drewc/GitHub/rh-website/rh.db'
    
# Server
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/drewxcom/rh.db'
    print("!!!!!!!! I'm using the server db path!")
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from flask_app.main.routes import main
from flask_app.manage.routes import manage
from flask_app.errors.handlers import errors

app.register_blueprint(main)
app.register_blueprint(manage)
app.register_blueprint(errors)

