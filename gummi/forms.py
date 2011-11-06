from wtforms import Form, TextField, validators

class RegisterChatRoom(Form):
    chatroom_name = TextField('Chatroom_name', \
                    [validators.Length(min=4, max=50),validators.NoneOf(\
                    "Enter Chat Room Name greater than 5 characters",\
                    message = "Please enter a value other than default value")])

