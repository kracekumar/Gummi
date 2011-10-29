from flask import Flask
app = Flask('gummi')
app.secret_key = 'h\xd8$\x81\x19%\xa2\xc9\xc2=\xeb\xf84wuv\xd4\xa3x%\x88\xfc\
\x92C\x1a]\xad\xfcC4\xe8,'
app.config['SQL_ALCHEMY_DATABASE'] = 'sqlite:////tmp/gummi.db'
import gummi.views
import gummi.database
