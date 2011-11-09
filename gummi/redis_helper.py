from datetime import datetime
from redis import Redis

redis_connection = Redis()

# Constants 
USERNAME = "username"
EMAIL = "email"
CHATROOM = "chatroom"
MESSAGES = "message"
COUNTER = "counter"

def build_chatroom_message_name(chatroom):
    """
       Builds key for redis to store chat room message in a list.
       :param chatroom: name of the chatroom
       Example: chatroom:python:message
       Here python is chatroom name
    """
    return ":".join([CHATROOM, chatroom, MESSAGES])

def build_chatroom_userlist(chatroom):
    """Builds key for redis to maintain list of users"""
    return ":".join([CHATROOM, chatroom, USERNAME])

def build_chatroom_message_user_counter(chatroom, username):
    """
        Builds key for redis counter to hold index of last accessed message
        for each user.
    """
    return ":".join([CHATROOM, chatroom, username, COUNTER])
   

def store_message(chatroom, message, username):
    """
      Messages exchanged in the chat room are stored inside chatroom are stored.
      Messages are stored as list in the format \
                                               chatroom:python:message
      :param chatroom: name of the chatroom
      :param message: chat message
      :param username: username who sent the message 
      
    """ 

    temp = redis_connection.pipeline()
    position = int(temp.rpush(build_chatroom_message_name(chatroom) ,message))
    temp.rpush(build_chatroom_userlist(chatroom), username)
    temp.setnx(build_chatroom_message_user_counter(chatroom, username), \
               position - 1)
    return temp.execute()

def fetch_message(chatroom, username):
    """Retrieve all messages from chatroom that doesn't belong to the user.

       :param chatroom: name of the chatroom
       :param username: current user 
    """
    chatroom_full_name = build_chatroom_message_name(chatroom)
    total_messages = redis_connection.llen(chatroom_full_name)
    counter_full_name = build_chatroom_message_user_counter(chatroom,)
    counter = int(redis_connection.get(counter_full_name))
    userlist_full = build_chatroom_userlist(chatroom)
    messages = []
    usernames = []
    if counter < total_messages - 1:
        for x in xrange(counter, total_messages):
            username_from_redis = redis_connection.lindex(userlist_full, x)
            if username_from_redis != username:
                messages.append(redis_connection.lindex(chatroom_full_name, x))
                usernames.append(username_from_redis)
            if x == total_messages - 1:
                redis_connection.set(counter_full_name, x)

    if messages:
        return messages, usernames
    else:
        return 0, 0



def add_user(username):
    """ Stores username of logged in user in a set.  """
    return redis_connection.sadd(USERNAME, username)

def check_username(username):
    """ Check whether user is already registered. """
    return redis_connection.sismember(USERNAME, username)

def add_chatroom(chatroom, creator):
    """ Creates chatroom and adds details like creator, created at in a dict.
        
        :param chatroom: name of the chatroom
        :param creator: username of the chatroom creator

    """
    temp = redis_connection.pipeline()
    temp.sadd(CHATROOM, chatroom)
    chatroom_details = CHATROOM + ":" +  chatroom  
    now = datetime.now()
    details = { "creator": creator, "created_at": "%d-%d-%d-%d-%d"%(now.day,\
                now.month, now.year, now.hour, now.minute) } 
    temp.hmset(chatroom_details, details)
    return temp.execute()

def get_all_chatroom():
    """ Returns list of currently avaiable chatrooms """
    names = redis_connection.smembers(CHATROOM)
    chatrooms = []
    for name in names:
        chatroom = { 'name': name }
        details = redis_connection.hgetall(CHATROOM + ":" + name)
        if details:
            chatroom['creator'] = details['creator']
            chatroom['created_at'] = details['created_at']
        chatrooms.append(chatroom)
    return chatrooms



def check_chatroom(chatroom_name):
    """ Check a chatroom already exists """
    return redis_connection.sismember(CHATROOM, chatroom_name)

