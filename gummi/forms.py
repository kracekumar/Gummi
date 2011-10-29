from wtforms import Form, TextField, validators

class RegisterChatRoom(Form):
    chatroom_name = TextField('Chatroom_name', \
                               [validators.Length(min=4, max=50)])

