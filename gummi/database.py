from gummi  import app
from flaskext.sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy(app)

class User(db.Model):
    """Holds Details all the User"""
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique = True)
    email = db.Column(db.String(120), unique = True)
    gender = db.Column(db.String(7))
    
    def __init__(self, username, email, gender):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


class ChatRoom(db.Model):
    """ :param name = chatroom name. E.G = python-dev chat
        :param id = id for each chatroom
        :param creator_id = foreign key to user table
        :param created_date = date of creation of chat room
    """
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(25), unique = True)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_datetime = db.Column(db.DateTime)
    user = db.relationship('User', \
                backref = db.backref('chatrooms', lazy='dynamic'))

    def __init__(self, name, user, created_datetime=None):
        self.name = name
        self.user = user
        if created_datetime is None:
            created_datetime = datetime.utcnow()
        self.created_datetime = created_datetime

    def __repr__(self):
        return '<ChatRoom %r>' % self.name


class ChatMessage(db.Model):
     """ :param id = chat message id.
         :param user_id = foreign key to table users.
         :param chatroom_id = foreign key to chatroom table.
         :param datetime = datetime the message was published.
     """
     id = db.Column(db.Integer, primary_key = True )
     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
     chatroom_id = db.Column(db.Integer, db.ForeignKey('chatroom.id'))
     message = db.Column(db.Text)
     datetime = db.Column(db.DateTime)

     user = db.relationship('User',\
                 backref = db.backref('users', lazy='dynamic'))
     chatroom = db.relationship('ChatRoom', \
                     backref = db.backref('chatrooms', lazy='dynamic'))

     def __init__(self, user_id, chatroom_id, message):
         self.user_id = user_id
         self.chatroom_id = chatroom_id
         self.message = message
         self.datetime = datetime.utcnow()

     def __repr__(self):
         return "<Message %r>" %self.message   

db.create_all()
