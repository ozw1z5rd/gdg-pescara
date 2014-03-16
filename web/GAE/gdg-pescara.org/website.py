#!/usr/bin/env python
# -*- coding: latin-1 -*-
# 
# file : website 
#
#  class Website : 
#    returns the default website application.
#
#
# see Main.py
#
from paragraph.Paragraph02 import *
from paragraph.Paragraph03 import *
from paragraph.Paragraph04 import *
from paragraph.Paragraph05 import *
from paragraph.Paragraph06 import *
from pageParts.Footer import *
from pageParts.Menu import *
from pageParts.Home import *
from error import * 
import os
from utility import Template
import webapp2
import logging
from google.appengine.api import users

# where 001
class Website(webapp2.RequestHandler):

    template = None

    def getTemplate( self):
        templateFile = os.path.join(
           os.path.dirname( __file__ ),
           'templates/index.template'
        )
        return  Template( templateFile )


    def get(self):

        user = users.get_current_user()
        login_url = users.create_login_url(self.request.path)
        logout_url = users.create_logout_url(self.request.path)

        if user is not None:
            logging.info("User come back [%s]" %(  user.email ) )

        template = self.getTemplate()
        if template is None:
            raise A1Exception( 
                WhatCode.TEMPLATE_EMPTY,
                WhereCode.WEBSITE_CLASS_GET_METHOD,
                WhyCode.UNKNOWN
            )

        indexHTML =template.render( 
             { 

               'pageNavbar'  : Menu().getContent( user, login_url, logout_url ),

               'pageHome' : Home().getContent(),

               'pageParagraph02' : 
                    { 'content'     : Paragraph02().getContent(), 
                      'title'       : Paragraph02().getTitle(),
                      'description' : Paragraph02().getDescription() 
                    }, 
              
               'pageParagraph03' : 
                    { 'content'     : Paragraph03().getContent(), 
                      'title'       : Paragraph03().getTitle(),
                      'description' : Paragraph03().getDescription()
                    },

               'pageParagraph04' : 
                    { 'content'     : Paragraph04().getContent(), 
                      'title'       : Paragraph04().getTitle(),
                      'description' : Paragraph04().getDescription()
                    },
               'pageParagraph05' : 
                    { 'content'     : Paragraph05().getContent(), 
                      'title'       : Paragraph05().getTitle(),
                      'description' : Paragraph05().getDescription()
                    },
               'pageParagraph06' : 
                    { 'content'     : Paragraph06().getContent(), 
                      'title'       : Paragraph06().getTitle(),
                      'description' : Paragraph06().getDescription()
                    },
                'pageFooter'  : Footer().getContent()
             }
        )

        self.response.write( indexHTML )

