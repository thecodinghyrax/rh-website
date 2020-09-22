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
if os.path.exists('/mnt/c/Users/drewc/OneDrive/Documents/GitHub/rh-website') or \
    os.path.exists('/mnt/c/Users/drewc/Code-Local/rh-website'):
    print("!!!!!!!! I'm using the local desktop db path.")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_PATH_LOCAL')

# Linux Desktop
elif os.path.exists('/home/drew/Code/rh-website'):
    print("!!!!!!!! I'm using the local Linux desktop db path.")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_PATH_LOCAL_LINUX')
        
# Server
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_PATH')
    app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    print("!!!!!!!! I'm using the server db path !!!!!")
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

############################################################
############################################################
######  Hey...you will need to delete all old messages when
###### Someone deletes their account the messages notification
###### will be stuck and people wont be able to clear it. fyi