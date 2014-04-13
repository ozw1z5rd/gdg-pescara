# # file : rest
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

    def decodeJson( self, jsonString ): 
        logging.info("E002 <- decodeJson")
        logging.info( jsonString )
        try:
            obj = json.loads( jsonString )
        except Exception, e:
            raise A1Exception(
                  WhereCode.REST_CLASS,
                  WhatCode.PARSE_ERROR,
                  WhyCode.MALFORMED_JSON )
        logging.info("Ok")
        logging.debug( obj )
        return obj
 
# mica tanto... non gestisce cose strutturate e per ora va bene 
# in questo modo. 
    def validateParams( self, jsonObj, modelObject ):
        for i in jsonObj.keys():
             if not i in dir( modelObject ):
                 raise A1Exception( 
                     WhereCode.REST_CLASS,
                     WhatCode.PARAMETER_ERROR, 
                     WhyCode.NOT_EXISTING_FIELD_IN_MODEL )
        # controllare la cardinalita' dei due insiemi 

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
           items = model.getListAll()
        for item in items:
            logging.info( item.title )
        pyData = ( { 'title' : x.title, 'description' : x.description, 'id' : x.key(), 'icon' : x.icon, 'techPage' : x.techPage }  for x in items )
        for item in pyData:
            logging.info( item )
        return self.response.write("doGet")

    def doPost( self, dct ):
        model = self.getModel( dct )
        pyData = self.decodeJson( self.request.body )
        self.validateParams( pyData, model )
        dataStoreObj = model.newFromDictionary( pyData )
        key = dataStoreObj.put()
        logging.debug( key )
        return self.response.write("doPost")

    def doDelete( self, dct ):
        model = self.getModel( dct )
        items = None
        if dct.has_key('eid'):
            logging.info("delete item %s from %s" % ( dct['eid'], dct['entity'] ))
        else:
            raise A1Exception( 
                WhereCode.REST_CLASS, 
                WhatCode.PARAMETER_ERROR,
                WhyCode.MISSING_ENTITY_ID )

        return self.response.write("doDelete")

    def doPut( self, dct ):
        model = self.getModel( dct )
        items = None
        if dct.has_key('eid'):
            logging.info("update item %s from %s" % ( dct['eid'], dct['entity'] ))
        else:
            raise A1Exception( 
                WhereCode.REST_CLASS, 
                WhatCode.PARAMETER_ERROR,
                WhyCode.MISSING_ENTITY_ID )

        return self.response.write("doPut")


