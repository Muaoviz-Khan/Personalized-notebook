from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db=SQLAlchemy()


def create_db(app,db):
    if not path.exists("app/instance/notebook.db"):
        with app.app_context():
            db.create_all()
            print("db created successfully")

def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']='very_secret'
    app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///notebook.db'
    db.init_app(app)

    from .auth.controllers.login import login
    app.register_blueprint(login,url_prefix='/api/auth')
    from .auth.controllers.logout import logout
    app.register_blueprint(logout,url_prefix='/api/auth')
    from .auth.controllers.register import register
    app.register_blueprint(register,url_prefix='/api/auth')

    from .notes.notebook import notess
    app.register_blueprint(notess,url_prefix='/api/notes')

    create_db(app,db)

    return app
