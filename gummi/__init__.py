from flask import Flask
from flaskext.sqlalchemy import SQLAlchemy
def create_app(name = __name__):
    app = Flask(name)
    app.config['SQL_ALCHEMY_DATABASE'] = 'sqlite:////tmp/gummi.db'
    db.init_app(app)
    return app

db = SQLAlchemy()
