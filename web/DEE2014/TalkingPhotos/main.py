#!/usr/bin/env python
# -*- coding: latin-1 -*-
#
#     This file is part of Talking Photos.
#
#     Talking Photos is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     Talking Photos is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with Talking Photos.  If not, see <http://www.gnu.org/licenses/>.
#
#     Alessio Palma / 2014
#     fb.com/alessio.palma
#     https://sites.google.com/site/ozw1z5rd/

import webapp2
from google.appengine.api import users, mail
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

