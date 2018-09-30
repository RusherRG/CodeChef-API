from flask import Flask
from config import Config

from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'any random string'

login = LoginManager(app)
login.login_view = 'login'
from app import routes