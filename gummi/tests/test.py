from flaskext.testing import TestCase
from flask import Flask
import unittest

from sys import path
from os  import chdir, getcwd 
chdir('../../')
path.append(getcwd())
import gummi.views as views

class Tests(TestCase):
    TESTING = True

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def runTest(self):
        self.create_app()


class AppTest(Tests):

    def test_get_user_name(self):
        """Initially user name is empty, we will check once again,
           after login"""
        print views.get_user_name() == None

    def runTest(self):
        self.test_get_user_name()

if __name__ == "__main__":
    unittest.main()
