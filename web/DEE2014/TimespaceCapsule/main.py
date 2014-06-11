#!/usr/bin/env python
# -*- coding: latin-1 -*-
#
import webapp2
from models import TimespaceCapsule
from google.appengine.api import users, mail
from template.AddCapsule import AddCapsuleFormTemplate, AddCapsuleKoTemplate, AddCapsuleOkTemplate
from template.OpenCapsule import OpenCapsuleTemplate
from template.RegisterCapsule import RegisterCapsuleErrorTemplate, RegisterCapsuleTemplate
from datetime import datetime
from decorators import login_required
from utilities import convert
import logging

logging.basicConfig()

class Home(webapp2.RequestHandler):
    pass

class OpenCapsule(webapp2.RequestHandler):
    """
    Gestisce l'apertura di una capsula
    """
    @login_required
    def get(self):
        user = users.get_current_user()
        tscid = [int(self.request.get('tscid'))]
        capsule = TimespaceCapsule().get_by_id(tscid)[0]
        lat   = convert(self.request, 'lat', 'float')
        lng   = convert(self.request,'lng', 'float')
        if capsule.requestToOpen( user, lat, lng ) == TimespaceCapsule.TSC_OK:
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
            body=body )
        capsule.setNotified()
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

    def post(self):
        #TODO convertire il tempo in utc prima di memorizzarlo.
        openDate = convert(self.request,'txtOpenDate', 'date')
        closeDate = convert(self.request,'txtCloseDate', 'date')
        content = convert(self.request,'txtContent', 'str' )
        lat = convert(self.request, 'txtLatitude', 'float')
        lng = convert(self.request, 'txtLongitude', 'float')
        tll = convert(self.request, 'txtTollerance', 'float')
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
    @login_required
    def get(self):
        tscid = [int(self.request.get('tscid'))]
        user = users.get_current_user()
        try:
            capsule = TimespaceCapsule.get_by_id(tscid)[0]
            logging.info(capsule)
        except Exception as e:
            logging.error(str(e))
            capsule = None

        if capsule is None or capsule.user is not None:
            message = 'Capsule not found'
            if capsule is not None:
                message += ' becayse is already assigned, sorry'
            page = RegisterCapsuleErrorTemplate({'message': message })
        else:
            capsule.user = user
            capsule.notifyDate = datetime.now()
            capsule.put()
            self.notifyUser(capsule)
            logoutUrl = users.create_logout_url("/register" )
            page = RegisterCapsuleTemplate({ 'logout' : logoutUrl })

        self.response.write( page.render() )

    def notifyUser(self, capsule ):
        mail.send_mail(
            sender="timespace_inc@noreply.com",
            to=capsule.user.email(),
            subject="Timespace capsule registered!",
            body="""you will be notified about capsule opening"""
            )

app = webapp2.WSGIApplication([
    ('/', Home),
    ('/register', RegisterCapsule ),
    ('/add', AddCapsule ),
    ('/open', OpenCapsule ),
    ('/cron', Cron )
], debug=True )
