from flaskext.testing import TestCase
from flask import Flask
import unittest

from sys import path
from os  import chdir, getcwd 
chdir('../../')
path.append(getcwd())

from gummi.views import get_user_name
from gummi.database import User, ChatMessage, db, ChatRoom

class Tests(TestCase):
    TESTING = True

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASEi_URI'] = 'sqlite:////temp/gummi_test.db'
        return app

    def runTest(self):
        self.create_app()


class AppTest(Tests):

    def test_get_user_name(self):
        """Initially user name is empty, we will check once again,
           after login"""
        print get_user_name() == None

    def test_add_user(username, email, gender):
        user = User(username, email, gender)
        db.session.add(user)
        db.commit(user)

    def runTest(self):
        self.test_get_user_name()
        self.test_add_user('krace', 'kracethekingmaker@gmail.com', 'male')
        self.test_add_user('', '', '')

if __name__ == "__main__":
    unittest.main()
