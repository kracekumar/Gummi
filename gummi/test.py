from flaskext.testing import TestCase
from flask import Flask
import views

class Tests(TestCase):

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
        assert views.get_user_name() == None

    def runTest(self):
        self.test_get_user_name()

test = AppTest()
t = Tests()
t.create_app()
test.runTest()

