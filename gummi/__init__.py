from flask import Flask
app = Flask('gummi')
app.secret_key =  '\xc3T\x06\x1fO\x84e\xda\xd4\xc0\xbey\\\x91\x82\x06\x97\xf5\
                    \xec\x8d\xb5\x84\xe8\x04f\x9f'
app.config['SQL_ALCHEMY_DATABASE'] = 'sqlite:////tmp/gummi.db'
import gummi.views
import gummi.database 


