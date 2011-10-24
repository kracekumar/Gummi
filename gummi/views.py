import json
from gummi import app
from flask import render_template, request, redirect, url_for, session
from flaskext.oauth import OAuth

FACEBOOK_APP_ID = "111665765610828"
FACEBOOK_APP_SECRET = "bb3f445f1a832bd24ba0a9bf2a0f5d63"

oauth = OAuth()

facebook = oauth.remote_app('facebook', 
    base_url='https://graph.facebook.com',
    request_token_url=None, 
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email'}
    )


def get_user_name():
    return session['user_name'] if session.has_key('user_name') else None

@app.route('/')
def index():
    return render_template('index.html', user_name = get_user_name())

@app.route('/chat/', methods = ["POST", "GET"])
def chat():
    return render_template('chat.html')

@app.route('/chatroom/<name>/', methods = ['POST', 'GET'])
def chatroom(name):
    if get_user_name():
        return render_template('chatroom.html')
    else:
        session['redirect_url'] = request.url
        return redirect(url_for('login'))

@app.route('/login', methods = ['POST', 'GET'])
def login():
    return facebook.authorize(callback=url_for('facebook_authorized',
           next=session['redirect_url'] or None,
           _external=True))

@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access Denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description'])
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    session['user_name'] = me.data['name']
    return redirect(url_for('welcome'))
    return 'Logged in as id=%s name=%s redirect=%s' %\
           (me.data['id'], me.data['name'], request.args.get('next'))

@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')

@app.route('/login/welcome/')
def welcome():
    return session['user_name'] 
