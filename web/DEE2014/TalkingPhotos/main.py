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
from template.visitorPageTemplate import VisitorActivatedDebugTemplate, \
VisitorActivatedErrorTemplate, VisitorActivatedTemplate, VisitorPageTemplate, \
VisitorWaitTemplate
from google.appengine.ext import db
from models import AllowedUser
import logging
logging.basicConfig()

ADMIN   = 'ozw1z5rd@gmail.com'
PENDING = -1
ACTIVE  =  1
DENIED  =  0

def login_required(function):
    def loginRequired(self):
        if users.get_current_user() is not None:
            function(self)
        else:
            loginUrl = users.create_login_url(dest_url=self.request.url)
            page = LoginPageTemplate({ 'login' : loginUrl })
            return self.response.write( page.render() )
    return loginRequired


class SendRequest( webapp2.RequestHandler):
    """
    Invia una richiesta, viene attivata dal visitatore verso il proprietario
    per poter attivare l'accesso ad una cerca risorsa
    Deve essere loggato per poter procedere
    """
    @login_required
    def get(self):
        user = users.get_current_user()
        if user is None:
            login_url = users.create_login_url( dest_url=self.request.path)
            page = LoginPageTemplate({ 'login' : login_url })
            return self.response.write( page.render() )

        userEmail = users.get_current_user().email()
        AllowedUser(email=userEmail, status = PENDING ).put() # pending
        logging.info("User %s messo in stato pendente " % userEmail )
        page = VisitorWaitTemplate({'logout': users.create_logout_url("/") })

        body = "Clicca per autorizzare : {0}/authorize?email={1}" \
            .format( self.request.host_url, userEmail )

        mail.send_mail(
            sender=ADMIN,
            to=ADMIN,
            subject="Nuova richiesta di autorizzazione",
            body=body )
        logging.info( body )
        return self.response.write( page.render())



class TalkingPhotos (webapp2.RequestHandler):
    """
    Questa è la class principale, quella che viene attivata quando si
    tenta di accedere alla risorsa.
    """
    @login_required
    def get(self):
        """
        1) ottiene l'utente corrente ( eventualmente chiedendogli di fare login )
        2) una volta che l'utente è loggato controlla il suo stato
        3) se attivo, mostra la pagina del contenuto
           se pending lo avvisa che deve attendere l'autorizzazione
           se non ha accesso viene chiesto di fare richiesta
        """
        status = self._allowed( users.get_current_user() )
        if status == ACTIVE :
            return self.homePage()
        elif status == PENDING:
            return self.visitorPendingPage()
        return self.visitorPage()

    def loginPage(self):
        """
        pagina di login, presenta la richiesta di login al visitatore
        """
        login_url = users.create_login_url( dest_url=self.request.path)
        page = LoginPageTemplate({ 'login' : login_url })
        return self.response.write( page.render() )

    def homePage(self):
        """
        pagina del contenuto.
        Per ora una pagina vuota ma può contentere tutto quello che vi vuole
        """
        logout_url = users.create_logout_url(self.request.path)
        nick = users.get_current_user().nickname()
        page = HomePageTemplate({ 'logout' : logout_url, 'user': nick })
        return self.response.write( page.render() )

    def visitorPage(self):
        """
        pagina di richiesta.
        Un utente non autorizzato può fare un richiesta per essere abilitato
        all'accesso
        """
        nick = users.get_current_user().nickname()
        logout_url = users.create_logout_url(self.request.path)
        page = VisitorPageTemplate({'authreq' : '/sendRequest', 'user' : nick, 'logout' : logout_url })
        return self.response.write( page.render() )

    def visitorPendingPage(self):
        """
        Pagina di cortesia. Viene visualizzata quando un visitatore, che non
        ha accesso e che ha fatto richiesta di autorizazione, prova di nuovo
        ad accedere alla risorsa.
        """
        logout_url = users.create_logout_url(dest_url=self.request.path)
        logging.info("######################")
        page = VisitorWaitTemplate({ 'logout' : logout_url })
        return self.response.write(page.render())

    def _allowed(self, who):
        """
        Ritorna lo stato di un utente
        0 : non autorizzato, può presentare richiesta di autorizzazione
        1 : autorizzato, può accedere alla risorsa
        -1: in attesa di autorizzazione, non può fare di nuovo richiesta
        """
        email = who.email()
        for allowed in AllowedUser.all():
            if email == allowed.email:
                status = allowed.status
                logging.info("%s status is %s " % ( email, status ))
                return allowed.status
        return 0

class _Reset(webapp2.RequestHandler):
    """
    Serve a caricare nel db l'utente di amministrazione
    essenzialmente ad uso interno.
    """
    @login_required
    def get(self):
        AllowedUser(email=ADMIN).put()
        return self.response.write("User Added")

class Authorize(webapp2.RequestHandler):
    """
    Pagina che può essere attivata solo dall'amministratore,
    autorizza un utente ad accedere alla risorsa.

    """
    @login_required
    def get(self):
        userToActivate = str(self.request.GET['email'])
        user = users.get_current_user().email()
        logout_url = users.create_logout_url(dest_url=self.request.host_url)
        params = { 'email' : userToActivate, 'logout' : logout_url }
        if user == ADMIN:
            record = db.Query( AllowedUser ).filter('email', userToActivate).fetch(1,0)[0]
            record.status = ACTIVE
            record.put() # errori non gestisti
            html = VisitorActivatedTemplate( params ).render()
            mail.send_mail(
                sender=ADMIN,
                to=userToActivate,
                subject="Sei stato attivato",
                body="Ora hai accesso alla risorsa" )

            logging.info("Email di notifica inviata")
        else:
            html = VisitorActivatedErrorTemplate(params).render()
        return self.response.write(html)


# path -> classe
app = webapp2.WSGIApplication([
    ('/', TalkingPhotos ),
    ('/sendRequest', SendRequest ),
    ('/reset', _Reset ),
    ('/authorize', Authorize )
], debug=True )

