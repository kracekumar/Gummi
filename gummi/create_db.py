import sys
print sys.path
from database import db
db.create_all()
