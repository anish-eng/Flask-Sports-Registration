
from flask_login import login_required,current_user,logout_user,LoginManager
from sqlalchemy import MetaData
from flask import Flask
from flask_mail import Mail
import os





from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash,generate_password_hash



import os

login_manager = LoginManager()
login_manager.login_view = '/'
login_manager.login_message_category = 'info'





app=Flask(__name__)
app.config["SECRET_KEY"]=ajdbeudeioddnuv9einfnv


basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



#db=SQLAlchemy(app)

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy(app)
login_manager.init_app(app)
from flask_migrate import Migrate

migrate=Migrate(app,db, render_as_batch=True)
app.config["MAIL_SERVER"]='smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail=Mail(app)
from schoolsports import routes