from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import os.path
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sitemap import Sitemap
from flask_mail import Mail



app = Flask(__name__)
# Desktop 
if os.path.exists('/mnt/c/Users/drewc/OneDrive/Documents/GitHub/rh-website'):
    print("!!!!!!!! I'm using the local desktop db path: ", os.getenv('DB_PATH'))
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/c/Users/drewc/OneDrive/Documents/GitHub/rh-website/rh.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_PATH')
    
# Laptop
elif os.path.exists('/mnt/c/Users/drewc/GitHub/rh-website'):
    print("!!!!!!!! I'm using the local laptop db path !!!!!!!!")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/c/Users/drewc/GitHub/rh-website/rh.db'
    
# Server
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/drewxcom/rh.db'
    print("!!!!!!!! I'm using the server db path !!!!!!!!")
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SITEMAP_URL_SCHEME'] = 'https'
app.config['MAIL_SERVER'] = 'smtp.pepipost.com'
app.config['MAIL_PORT'] = 25 
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASS')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'
ext = Sitemap(app=app)
mail = Mail(app)



from flask_app.main.routes import main
from flask_app.manage.routes import manage
from flask_app.errors.handlers import errors

app.register_blueprint(main)
app.register_blueprint(manage)
app.register_blueprint(errors)

