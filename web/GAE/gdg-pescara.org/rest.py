#
# file : rest
#
#    class : Api ( restfull interface )
#
# see Main.py
#
#
#
#
#
#
#


import webapp2
from model import *
from error import * 
import json 
import logging 
from google.appengine.ext import db

# where 002
class Api( webapp2.RequestHandler ):

    def get( self ): 
        logging.info("got a new api request")
        return self.response.write("TODO")







