from gummi import app
from flask import render_template, request, redirect, url_for, session, flash
from flaskext.oauth import OAuth
from forms import RegisterChatRoom
from database import User, ChatRoom, ChatMessage, db

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

@app.route('/chat/', methods = ["POST", "GET"])
def chat():
    return render_template('chat.html')

@app.route('/chatroom/<name>/', methods = ['POST', 'GET'])
def chatroom(name):
    """ Actual chat room handling function but not complete """
    if get_user_name():
        return render_template('chatroom.html')
    else:
        session['redirect_url'] = request.url
        return redirect(url_for('login'))

@app.route('/login', methods = ['POST', 'GET'])
def login():
    """ Facebook Login"""
    return facebook.authorize(callback=url_for('facebook_authorized',
           next=None or request.args['next'],
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

    if not check_user(email):
        add_user(session['user_name'], email, gender) 

    return redirect(url_for('%s'%request.args['next']))
    return 'Logged in as email=%s name=%s gender=%s, added to db =%s' %\
           (email, session['user_name'], gender, check_user(email))

@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')

@app.route('/login/welcome/')
def welcome():
    """ Welcome page after login, it is here for test """ 
    return session['user_name'] 

def add_to_session(session_object):
    db.session.add(session_object)
    return db.session.commit()

def check_user(email):
    return True if User.query.filter_by(email = email).first() else False

def add_user(user_name, email, gender):
    user = User(user_name, email, gender)
    add_to_session(user)

def check_chatroom(name):
    return True if ChatRoom.query.filter_by(name = name).first() else False

def add_chatroom(name, user_id):
    chatroom = ChatRoom(name, user_id)
    return add_to_session(chatroom)

def get_all_chatroom():
    return db.session.query(ChatRoom).all()

@app.route('/chatroom/register/', methods = ['POST', 'GET'])
def register():
    if get_user_name():
        form = RegisterChatRoom(request.form)
        if request.method == 'POST' and form.validate():
            user = User.query.filter_by(username = session['user_name']).first()
            chatroom_name = form.chatroom_name.data
            if not check_chatroom(chatroom_name):
                if add_chatroom(chatroom_name, user.id):
                    flash(chatroom_name + "added ")
                    return render_template('register.html', form=form, \
                                        chatrooms=get_all_chatroom())
        return render_template('register.html', form=form, \
                                      chatrooms=get_all_chatroom())
    else:
        return redirect(url_for('login?next=register'))
