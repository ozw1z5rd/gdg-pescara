#
# runOnce / Init 
#
# initialize the whole application setting the data, will reset anything
#
import webapp2
import os
from google.appengine.api import users
from google.appengine.ext import db 
import logging

# where 003
class Init( webapp2.RequestHandler ):
    def get( self ):
        user = users.get_current_user()
        if user is None:
            self.response.abort('404')
        logging.info("User [%s] requested the application init" % ( user  ) ) 
    
    
