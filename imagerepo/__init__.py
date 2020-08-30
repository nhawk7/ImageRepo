from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from imagerepo import Config

app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from imagerepo import routes
