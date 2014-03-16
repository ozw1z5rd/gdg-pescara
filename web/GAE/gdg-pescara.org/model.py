# -*- coding: latin-1 -*-

from google.appengine.ext import db 
from google.appengine.api import users

#
# just an icon 
# a link to a webpage
# a short description
# rating ( skill level ) 
#
class Technology( db.Model ):
    icon = db.BlobProperty()
    techPage = db.LinkProperty()
    description = db.TextProperty()

#
# middle earth :-) 
#
class Rating( db.Model ):
    tech = db.ReferenceProperty( Technology )     
    rating = db.RatingProperty()

#
# G+ user
# link to G+ page
# email 
# phone 
# tech he loves ( a list )
# short description
# 
class Profile( db.Model ):
    user  = db.UserProperty()
    gPage = db.LinkProperty()
    email = db.EmailProperty()
    phone = db.PhoneNumberProperty()
    techList = db.ListProperty( db.Key )
    description = db.TextProperty()
    lastAccess = db.DateTimeProperty()

#
# not yet used.
#
class Paragraph( db.Model ):
    number = db.IntegerProperty()
    title  = db.StringProperty()
    description = db.StringProperty()
    content = db.TextProperty()

