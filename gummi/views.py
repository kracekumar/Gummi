from gummi import app
from flask import render_template, request, redirect, url_for, session, flash
from flask import Markup, jsonify
from flaskext.oauth import OAuth
from forms import RegisterChatRoom
from database import User, ChatRoom, ChatMessage, db
from redis_helper import add_user, check_username, add_chatroom,\
                         get_all_chatroom, check_chatroom, store_message,\
                         fetch_message

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
    """ Fetch the logged in User"""
    return session['user_name'] if session.has_key('user_name') else None

@app.route('/')
def index():
    return render_template('index.html', user_name = get_user_name())

@app.route('/chatroom/<channel>/send/', methods = ["POST", "GET"])
def send(channel, username = None , message = None):
    if request.method == "GET":
#        print message, channel
        username = Markup(request.args.get('username', type=str))
        channel = Markup(request.args.get('channel', type=str))
        messages, usernames = fetch_message(channel, username)
        print jsonify(messages=messages)
        if messages:
            return jsonify(messages=messages, usernames=usernames, success=1)
        else:
            return jsonify(messages='false', usernames='false', success=0)
    else:
        message, usernames = fetch_message(channel, username, success=1)
        if messages:
            return jsonify(messages=messages, usernames=usernames, success=0)
        else:
            return jsonify(messages='false', usernames='false')
    

@app.route('/chatroom/<name>/publish/', methods = ["POST", "GET"])
def publish(name):
    if request.method == "GET":
        channel_to = Markup(request.args.get('channel',  type=str))
        message = Markup(request.args.get('message',  type=str))
        username = Markup(request.args.get('user', type=str))
        store_message(channel_to, message, username)
        send(channel_to, username, message)
        return render_template('success.html')
    

     

@app.route('/chatroom/<name>/', methods = ['POST', 'GET'])
def chatroom(name):
    """ Actual chat room handling function but not complete """
    if get_user_name():
        if check_chatroom(name):
            return render_template('chat.html', \
                                        room=name,username=session['user_name'])
        else:
            return redirect(url_for('register'), username=session['user_name'])
    else:
        session['next'] = url_for('chatroom', name=name)
        return redirect(url_for('login'))

@app.route('/login', methods = ['POST', 'GET'])
def login():
    """ Facebook Login"""
    return facebook.authorize(callback=url_for('facebook_authorized',
           next=None or  session['next'],
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
    session['email'] = me.data['email']
    email = me.data['email']
    gender = me.data['gender']

    if not check_username(session['user_name']):
        add_user(session['user_name']) 
    
    if session['next']:
       return redirect(session['next'])

    return redirect( url_for('register'))

@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')


@app.route('/chatroom/register/', methods = ['POST', 'GET'])
def register():
    if get_user_name():
        form = RegisterChatRoom(request.form)
        if request.method == 'POST' and form.validate():
            chatroom_name = form.chatroom_name.data
            if not check_chatroom(chatroom_name):
                if add_chatroom(chatroom_name, session['user_name']):
                    flash(chatroom_name + " successfully added ")
                    return render_template('register.html', form=form, \
                        chatrooms=get_all_chatroom(), username=get_user_name())

        return render_template('register.html', form=form, \
                        chatrooms=get_all_chatroom(), username=get_user_name())
    else:
        session['next'] = url_for('register')
        return redirect(url_for('login'))
