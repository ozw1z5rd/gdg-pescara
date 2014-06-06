#!/usr/bin/env python
# -*- coding: latin-1 -*-
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from google.appengine.api import users
from template.loginPageTemplate import LoginPageTemplate
from template.homePageTemplate import HomePageTemplate
from template.visitorPageTemplate import *
from google.appengine.ext import db
import pprint

from models import AllowedUser

import logging
logging.basicConfig()
# from ... import mail
ADMIN   = 'ozw1z5rd@gmail.com'
PENDING = -1
ACTIVE  =  1
DENIED  =  0

class SendRequest( webapp2.RequestHandler):
    def get(self):
        userEmail = users.get_current_user().email()
        AllowedUser(email=userEmail, status = PENDING ).put() # pending
        logging.info("User %s messo in stato pendente " % userEmail )
        page = VisitorActivatedDebugTemplate({'email':userEmail})
        return self.response.write( page.render())



class TalkingPhotos (webapp2.RequestHandler):
    # pagina dove l'utente deve loggare
    def loginPage(self):
        login_url = users.create_login_url(self.request.path)
        page = LoginPageTemplate({ 'login' : login_url })
        return self.response.write( page.render() )

    # home page con tutti i crismi del caso per un utente autorizzato
    def homePage(self):
        logout_url = users.create_logout_url(self.request.path)
        nick = users.get_current_user().nickname()
        page = HomePageTemplate({ 'logout' : logout_url, 'user': nick })
        return self.response.write( page.render() )

    # pagina per gli utenti che vogliono accedere alla risorsa ma devono
    # essere autorizzati
    def visitorPage(self):
        nick = users.get_current_user().nickname()
        logout_url = users.create_logout_url(self.request.path)
        page = VisitorPageTemplate({'authreq' : '/sendRequest', 'user' : nick, 'logout' : logout_url })
        return self.response.write( page.render() )

    def visitorPendingPage(self):
        logout_url = users.create_logout_url(self.request.path)
        page = VisitorWaitTemplate({ 'logout' : logout_url })
        return self.response.write(page.render())

    # ritorna true per tutti gli utenti che sono autorizzati
    #  0 : not auth.
    #  1 : auth
    # -1 : pending
    def allowed(self, who):
        email = who.email()
        for allowed in AllowedUser.all():
            if email == allowed.email:
                status = allowed.status
                logging.info("%s status is %s " % ( email, status ))
                return allowed.status
        return 0

    def get(self):
        user = users.get_current_user( )
        if user is None:
            return self.loginPage()
        status = self.allowed( user )
        if status == ACTIVE :
            return self.homePage()
        elif status == PENDING:
            return self.visitorPendingPage()
        return self.visitorPage()

class Reset(webapp2.RequestHandler):
    def get(self):
        AllowedUser(email=ADMIN).put()
        return self.response.write("User Added")

class Authorize(webapp2.RequestHandler):
    # autorizza l'utente
    def get(self):
        userToActivate = str(self.request.GET['email'])
        user = users.get_current_user().email()
        params = { 'email' : userToActivate }
        if user == ADMIN:
            record = db.Query( AllowedUser ).filter('email', userToActivate).fetch(1,0)[0]
            record.status = ACTIVE
            record.put() # errori non gestisti
            html = VisitorActivatedTemplate( params).render()
        else:
            html = VisitorActivatedErrorTemplate(params).render()
        return self.response.write(html)

app = webapp2.WSGIApplication([
    ('/', TalkingPhotos ),
    ('/sendRequest', SendRequest ),
    ('/reset', Reset ),
    ('/authorize', Authorize )
], debug=True )

