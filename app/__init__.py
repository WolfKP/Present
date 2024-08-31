from flask import Flask
from .extensions import db, bcrypt, login_manager, mail
from .routes import main

def create_app():

    app= Flask(__name__, instance_relative_config= True)
    app.config.from_pyfile("config.py")
    
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    db.init_app(app)

    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app
