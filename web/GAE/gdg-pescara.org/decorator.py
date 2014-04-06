from google.appengine.api import users
import logging
from error import *

def authRequired( func ):
    def requireUser( self, **dict ):
        current_user = users.get_current_user()
        if current_user is None:
           raise S1Exception( 
               WhatCode.AUTH,
               WhereCode.REST_CLASS,
               WhyCode.NO_USER_PROVIDED
           )
        elif not str(current_user) in ( 'ozw1z5rd', 'antonello.pinella' ):
            logging.warning("E002 RW attempt from [%s]" % ( current_user ))
            raise S1Exception(
               WhatCode.AUTH,
               WhereCode.REST_CLASS,
               WhyCode.NO_VALID_USER_PROVIDED
            )
        logging.info("E002 RW GRANTED TO [%s]"%(current_user));
        return func(self, **dict)
    return requireUser 


