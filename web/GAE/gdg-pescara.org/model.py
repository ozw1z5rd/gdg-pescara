# -*- coding: latin-1 -*-

from google.appengine.ext import db 
from google.appengine.api import users
import logging 
import json 


# Forse dovrebbe anche smazzarsi il parsing del json e 
# tornare un oggetto ad hoc.

#
# just an icon 
# a link to a webpage
# a short description
# rating ( skill level ) 
#
class Technology( db.Model ):
    #eid= db.IntegerProperty()
    icon = db.BlobProperty()
    techPage = db.LinkProperty()
    title = db.TextProperty()
    description = db.TextProperty()

    @staticmethod
    def newFromDictionary( dct ):
        logging.debug( dct )
        return Technology( 
            icon = str(dct['icon']), 
            techPage = dct['techPage'], 
            description = dct['description'],
            title = dct['title']  ) 

    @staticmethod
    def serializeToJSON( self ):
        pass

    @staticmethod
    def getListAll( ) : 
        items = db.Query( Technology ).fetch( limit = 100 )
        return items

# experimental
    @staticmethod
    def getKey(  ):
        return "title"
#
# middle earth :-) 
#
class Rating( db.Model ):
    #eid= db.IntegerProperty()
    tech = db.ReferenceProperty( Technology )     
    rating = db.RatingProperty()

    @staticmethod
    def newFromDictionary( dct ):
        logging.debug( dct )
        # si deve recuperare l'id della tecnologia che poi deve essere caricata
        return Rating( tech = str(dct['tech']) , rating = int(dct['rating']) )

    def serializeToJSON( self ):
        pyData = { 
            'tech' : self.tech, 
            'rating' : self.rating, 
             '_key' : self.key() }

        return json.dumps( pyData )

#
# G+ user
# link to G+ page
# email 
# phone 
# tech he loves ( a list )
# short description
# 
class Profile( db.Model ):
    #eid= db.IntegerProperty()
    user  = db.UserProperty()
    gPage = db.LinkProperty()
    email = db.EmailProperty()
    phone = db.PhoneNumberProperty()
    techList = db.ListProperty( db.Key )
    description = db.TextProperty()
    lastAccess = db.DateTimeProperty()

    def serializeToJSON( self ):
        pyData = { 
            '_key' : self.key(),
            'user' : self.user.email, 
            'gpage' : self.gPage, 
            'phone' : self.phone, 
            'description' : self.description, 
            'lastAccess' : self.DateTimeProperty }
        return json.dumps( pyData )
            

#
# not yet used.
#
class Paragraph( db.Model ):
    #eid= db.IntegerProperty()
    number = db.IntegerProperty()
    title  = db.StringProperty()
    description = db.StringProperty()
    content = db.TextProperty()

    @staticmethod
    def newFromDictionary( dct ):
        logging.debug( dct )
        return Paragraph( 
            number = int( dct['number'] ), 
            title  = dct['titile'],
            description = dct['description'],
            content = dct['content'] )

    def serializeToJSON( self ):
        pyData = {
            'number' : self.number, 
            'title' : self.title,
            'description' : self.description, 
            'content' : self.content, 
            '_key' : self.key() }

#
# the index section
#
class Content(db.Model):
    #eid= db.IntegerProperty()
    description=db.TextProperty()
    reference=db.LinkProperty()

    @staticmethod
    def newFromDictionary( dct ):
        logging.debug( dct )
        return Paragraph( 
            number = int( dct[''] ), 
            description = dct['description'],
            reference = dct['reference'] )

    def serializeToJSON( self ):
        pass
   
