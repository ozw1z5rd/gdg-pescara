from google.appengine.ext import db

class AllowedUser (db.Model):
    email = db.EmailProperty()
    status = db.IntegerProperty() # 0 : no, 1: si, -1 : pending
