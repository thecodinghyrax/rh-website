from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import os.path



app = Flask(__name__)
if os.path.exists('/mnt/c/Users/drewc/Documents/GitHub/rh-web/rh.db'):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/c/Users/drewc/Documents/GitHub/rh-web/rh.db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/drewxcom/rh.db'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
db = SQLAlchemy(app)

from flask_app import routes
