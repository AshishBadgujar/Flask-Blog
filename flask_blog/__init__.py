from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app=Flask(__name__)

app.config['SECRET_KEY']='b3b0409d3946ce228b90650845a54f64'

bcrypt=Bcrypt(app)
login_manager=LoginManager(app)

from flask_blog import routes

