from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

bcrypt= Bcrypt()
login_manager= LoginManager()
mail= Mail()
db= SQLAlchemy()

login_manager.login_view= "main.login"