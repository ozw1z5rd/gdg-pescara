#
# file : rest
#
#    class : Api ( restfull interface )
#    
#
# see Main.py
#
from google.appengine.api import users
import webapp2
from error import * 
from model import *
import json 
import logging 
# says if someone can access or not the method
from decorator import authRequired


# where 002
class Api( webapp2.RequestHandler ):

    string2Class = { 
       'technology' : Technology,
       'rating' : Rating,
       'profile' : Profile,
       'paragraph' : Paragraph,
       'content' : Content
    }

    def getModel( self, dct ):
        """
        Return the class ( object )
        """
        logging.info( dct )
        if dct.has_key('entity') :
            modelName = dct['entity']
            logging.info("E002 <- model [%s]" % ( modelName ))
            if modelName in self.string2Class.keys() :
                return self.string2Class[modelName]
            raise A1Exception(
                  WhereCode.REST_CLASS_GETMODEL_METHOD,
                  WhatCode.PARAMETER_ERROR,
                  WhyCode.MODEL_NOT_AVAILABLE )
        raise A1Exception( 
              WhereCode.REST_CLASS_GETMODEL_METHOD,
              WhatCode.PARAMETER_ERROR,
              WhyCode.PARAMETER_VALUE_ERROR)

    def get( self, *arg, **dct ): 
        logging.info("E002 <-GET")
        return self.doGet( dct )

    @authRequired
    def put( self, **dct ):
        logging.info("E002 <-PUT")
        logging.info( dct )
        return self.doPut( dct )

    @authRequired
    def post( self, **dct ):
        logging.info("E002 <-POST")
        logging.info( dct )
        return self.doPost( dct )

    @authRequired
    def delete( self, **dct ):
        logging.info("E002 <-DELETE")
        logging.info( dct )
        return self.doDelete( dct )

    def doGet( self, dct ):
        logging.info( dct )
        model = self.getModel( dct )
        items = None
        if dct.has_key('eid') :
           logging.info("richiesta di un id specifico") 
        else:
           items = model.all()
        logging.info( items )
        return self.response.write("doGet")

    def doPost( self ):
        logging.info("not implemented")
        return self.response.write("doPost")

    def doDelete( self, dct ):
        return self.response.write("doDelete")

    def doPut( self, dct ):
        return self.response.write("doPut")


