#!/usr/bin/env python
# -*- coding: latin-1 -*-
#
import webapp2
from models import *
from google.appengine.api import users, mail
from template import *
from template.AddCapsule import *
from template.OpenCapsule import *
from template.RegisterCapsule import *
from datetime import datetime
import logging

logging.basicConfig()
TIMEFORMAT = "%d/%m/%Y" # 31/01/2010

class Home(webapp2.RequestHandler):
    pass

class OpenCapsule(webapp2.RequestHandler):
    """
    Gestisce l'apertura di una capsula
    """
    def get(self):
        user = users.get_current_user()
        tscid = [int(self.request.get('tscid'))]
        capsule = TimespaceCapsule().get(tscid)[0]
        lat   = self.GET.get('lat')
        lng   = self.GET.get('lng')
        if capsule.requestOpen( user, lat, lng ) == TimespaceCapsule.TSC_OK:
            page = OpenCapsuleTemplate({ 'content' : capsule.show() })
            return self.response.write( page.render())


class Cron(webapp2.RequestHandler):
    """
    Gestisce il cron per l'invio dei messaggi
    """

    def _sendMail(self, capsule):

        body="You Got A Message From Past "
        if capsule.positionLat is not None and capsule.positionLng is not None:
            body += "and you can open this at lan=%s lng=%s" % \
                ( capsule.positionLat, capsule.positionLng)
        body += " /open?tscid=%s" % str(capsule.key().id())

        mail.send_mail(
            sender="timespace_inc@noreply.com",
            to=capsule.user.email(),
            subject="You Got A Message From Past",
            body=body
            )
        logging.info(body)

    def get(self):
        allCapsule = TimespaceCapsule().all()
        for capsule in allCapsule:
            if capsule.openingDate < datetime.now():
                if capsule.closingDate > datetime.now():
                    if capsule.user is not None:
                        self._sendMail( capsule )
        return self.response.write("")



class AddCapsule(webapp2.RequestHandler):
    """
    Aggiunge una nuova capsula non registrata
    """

    def convert(self, key, t):
        value = self.request.get(key)
        logging.info("%s %s" %( key, value) )
        if value is None or len(value) == 0:
            return None
        if t == 'str':
            return str(value)
        elif t == 'float':
            return float(value)
        elif t == 'date':
            return datetime.strptime(value, TIMEFORMAT )
        return None

        return self.request.get(key)

    def post(self):
        #TODO convertire il tempo in utc prima di memorizzarlo.
        openDate = self.convert('txtOpenDate', 'date')
        closeDate = self.convert('txtCloseDate', 'date')
        content = self.convert('txtContent', 'str' )
        lat = self.convert( 'txtLatitude', 'float')
        lng = self.convert( 'txtLongitude', 'float')
        tll = self.convert( 'txtTollerance', 'float')
        try:
            tsc =  TimespaceCapsule( openingDate = openDate,
                closingDate=closeDate, content=content,
                positionLat = lat, positionLng = lng,
                positionTll = tll )
            tsc.put()
        except Exception as e:
            logging.error(str(e))
            page = AddCapsuleKoTemplate({})
        else:
            page = AddCapsuleOkTemplate({
                'tscid' : str(tsc.key(),id()),
                'openingDate' : tsc.openingDate.strftime("%d-%m-%Y"),
                'closingDate' : tsc.closingDate.strftime("%d-%m-%Y"),
                'content' : tsc.content,
                'latitude' : tsc.positionLat or "none",
                'longitude' : tsc.positionLng or "none",
                'tollerance' : tsc.positionTll or "none"})

        return self.response.write(page.render())

    def get(self):
        page = AddCapsuleFormTemplate({})
        self.response.write(page.render())

class RegisterCapsule(webapp2.RequestHandler):
    """
    Registra ( associa ) una capsula ad un utente
    """
    def get(self):
        user = users.get_current_user()
        if user is None:
            loginUrl = users.create_login_url(dest_url='/register')
            logging.info("login page, user is not logged")
            page = RegisterCapsuleLoginTemplate({ 'login' : loginUrl })
        else:
            tscid = [int(self.request.get('tscid'))]
            try:
                capsule = TimespaceCapsule.get_by_id(tscid)[0]
                logging.info(capsule)
            except Exception as e:
                logging.error(str(e))
                capsule = None

            if capsule is None or capsule.user is not None:
                message = 'Capsule not found'
                if capsule.user is not None:
                    message += ' already assigned, sorry'
                page = RegisterCapsuleErrorTemplate({'message': message })
            else:
                capsule.user = user
                capsule.notifyDate = datetime.now()
                capsule.put()
                logoutUrl = users.create_logout_url("/register" )
                page = RegisterCapsuleTemplate({ 'logout' : logoutUrl })

        self.response.write( page.render() )

app = webapp2.WSGIApplication([
    ('/', Home),
    ('/register', RegisterCapsule ),
    ('/add', AddCapsule ),
    ('/open', OpenCapsule ),
    ('/cron', Cron )
], debug=True )





































