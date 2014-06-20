#!/usr/bin/env python
# -*- coding: latin-1 -*-
#
#     This file is part of Timespace Capsule.
#
#     Timespace Capsule is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     Timespace Capsule is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with Timespace Capsule.  If not, see <http://www.gnu.org/licenses/>.
#
#     Alessio Palma / 2014
#     fb.com/alessio.palma
#     https://sites.google.com/site/ozw1z5rd/


import webapp2
from urllib2 import quote
from models import TimespaceCapsule
from google.appengine.api import users, mail
from template.AddCapsule import AddCapsuleFormTemplate, AddCapsuleKoTemplate, AddCapsuleOkTemplate
from template.OpenCapsule import OpenCapsuleTemplate, OpenCapsuleErrorTemplate,\
    OpenCapsuleErrorTemplateNoGeo
from template.RegisterCapsule import RegisterCapsuleErrorTemplate, RegisterCapsuleTemplate
from template.Home import HomeTemplate
from template.Geolocation import GeolocationTemplate
from datetime import datetime
from decorators import login_required
from utilities import convert, date2String
import logging

logging.basicConfig()

class Home(webapp2.RequestHandler):
    def get(self):
        urls= {
            'add_url' : '/add', \
            'open_url' : '/open', \
            'register_url' : '/register'\
        }

        html = "<ul>"
        for capsule in TimespaceCapsule.all():
            id = capsule.key().id()
            logging.info("capusula. {0}".format(id))
            openD = date2String(capsule.openingDate)
            close = date2String(capsule.closingDate)
            notify = date2String(capsule.notifyDate)
            seen = "yes" if capsule.seen else "not yet"
            lastSeenDate = date2String(capsule.lastSeenDate)
            assigned = "no"
            if capsule.user is not None:
                assigned = "yes"
            if capsule.anonymous:
                assigned = 'anon'
            geolocated = "yes" if capsule.positionLat else "no"
            if not capsule.seen:
                color = "red"
            else:
                color = "black"

            html += """<li><font color='{0}'><b>{1}</b></font>
                      O:<b>{2}</b> C:<b>{3}</b> notify:<b>{4}</b>
                      seen:<b>{5}</b> sdate:<b>{6}</b>,
                      assigned:<b>{7}</b>, geolocated:<b>{8}</b>
                """.format( color, id, openD, close, notify, seen, \
                            lastSeenDate, assigned, geolocated)

        html += '</ul>'
        urls.update({ 'html' : html })
        page = HomeTemplate( urls )
        return self.response.write(page.render());


class Cron(webapp2.RequestHandler):
    """
    Gestisce il cron per l'invio dei messaggi
    """
    def _sendMail(self, capsule):

        body="You Got A Message From Past click to open"
        if capsule.positionLat is not None and capsule.positionLng is not None:
            body += "http://timespacecapsule.appspot.com/activate?tscid={1}&lat=0&lan=0"\
                .format( self.request.host_url, str(capsule.key().id()))

        mail.send_mail(
            sender="ozw1z5rd@gmail.com",
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
        reg = convert(self.request, "chkAnonymous", 'boolean')
        try:
            tsc =  TimespaceCapsule( openingDate = openDate,
                closingDate=closeDate, content=content,
                positionLat = lat, positionLng = lng,
                positionTll = tll, anonymous=reg )
            tsc.put()
        except Exception as e:
            logging.error(str(e))
            page = AddCapsuleKoTemplate({})
        else:
            tscid = str(tsc.key().id())
            link = "{0}/activate?tscid={1}&lat=0&lng=0".format(self.request.host_url,tscid)
            page = AddCapsuleOkTemplate({
                'tscid' : tscid,
                'openingDate' : date2String(tsc.openingDate),
                'closingDate' : date2String(tsc.closingDate),
                'content' : tsc.content,
                'anonymous' :  "yes" if tsc.anonymous else "no",
                'latitude' : tsc.positionLat or "none",
                'longitude' : tsc.positionLng or "none",
                'link' : link,
                'enc_link' : quote(link),
                'tollerance' : tsc.positionTll or "none"})

        return self.response.write(page.render())

    def get(self):
        page = AddCapsuleFormTemplate({})
        self.response.write(page.render())


class Activate(webapp2.RequestHandler):
    """
    Registra ( associa ) una capsula ad un utente
    se non associata e la modalità è anonima tenta l'apertura
    se associata e l'utente è corretto prova l'apertura
    """

    def _tryOpen(self, user, tscid, capsule ):

        lat   = convert(self.request, 'lat', 'float')
        lng   = convert(self.request,'lng', 'float')

        logging.info(lat)
        logging.info(lng)

        message = "This capsule is not bound to any position"
        if capsule.positionLat is not None:
            message="This capsule is bound to a position {0},{1}"\
                .format(capsule.positionLat, capsule.positionLng)

        responseParameters = { \
            'openingDate' : date2String(capsule.openingDate), \
            'closingDate' : date2String(capsule.closingDate),\
            'space' : message,
            'tscid' : tscid[0],
            'host' : self.request.host_url,
        }

        tscCode = capsule.requestToOpen( user, lat, lng )

        if tscCode == TimespaceCapsule.TSC_OK:
            page = OpenCapsuleTemplate({ 'content' : capsule.show() })
            return self.response.write( page.render())
        else:
            if tscCode == TimespaceCapsule.TSC_TOOSOON:
                message = "Too soon! opening date is {0}"\
                    .format( capsule.openingDate.strftime("%d/%m/%Y"))
            elif tscCode == TimespaceCapsule.TSC_TOOLATE:
                message = "Too late! Capsule expired on {0}"\
                    .format(capsule.closingDate.strftime("%d/%m/%Y"))
            elif tscCode == TimespaceCapsule.TSC_BADUSER:
                message= "Registered to different user"
            elif tscCode == TimespaceCapsule.TSC_NOTASSIGNED:
                message="not yet assigned"
            elif tscCode == TimespaceCapsule.TSC_TOODISTANT:
                message = "You are far away from the opening point {0},{1}"\
                    .format( capsule.positionLat, capsule.positionLng )
            elif tscCode == TimespaceCapsule.TSC_LATLNG:
                message = "to open this capsule you have to provide a position"

        responseParameters.update( { 'message' : message })
        if capsule.positionLat is None or capsule.positionLng is None:
            page = OpenCapsuleErrorTemplateNoGeo(responseParameters)
        else:
            page = OpenCapsuleErrorTemplate(responseParameters)

        self.response.write( page.render() )

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

        if capsule is None:
            message = 'Capsule not found'
            page = RegisterCapsuleErrorTemplate({'message': message })

        if capsule.anonymous:
            return self._tryOpen(user, tscid, capsule )

        if capsule.user is None:
            capsule.user = user
            capsule.notifyDate = datetime.now()
            capsule.put()
            self.notifyUser(capsule)
            logoutUrl = users.create_logout_url("/register" )
            page = RegisterCapsuleTemplate({ 'logout' : logoutUrl })
        elif capsule.user != user:
            message = 'capsule is already assigned, sorry'
            page = RegisterCapsuleErrorTemplate({'message': message })
        else:
            return self._tryOpen(user,tscid, capsule )
        self.response.write( page.render() )

    def notifyUser(self, capsule ):
        mail.send_mail(
            sender="ozw1z5rd@gmail.com",
            to=capsule.user.email(),
            subject="Timespace capsule registered!",
            body="""you will be notified about capsule opening"""
            )

class Radar(webapp2.RequestHandler):
    """
    returns how far is this capsule
    """
    def get(self):
        tscid = [int(self.request.get('tscid'))]
        lat   = convert(self.request, 'lat', 'float')
        lng   = convert(self.request,'lng', 'float')
        if lng is None or lat is None:
            rc = "-2|"
        try:
            obj = TimespaceCapsule.get_by_id(tscid)[0]
        except Exception as e:
            logging.warn(str(e))
            obj = None
        if obj is None:
            rc = '-1|'
        else:
            distance = obj.distance(lat,lng)
            if distance < 1000:
                strDistance = str(distance) + " meters"
            else:
                strDistance = str(distance/1000.0) + " Km"
            rc = "0|"+str(strDistance)
        return self.response.write(rc)

class Test(webapp2.RequestHandler):
    def get(self):
        page = GeolocationTemplate({})
        return self.response.write( page.render() )

app = webapp2.WSGIApplication([
    ('/test', Test),
    ('/radar', Radar),
    ('/', Home),
    ('/activate', Activate ), # gestisce il ciclo della capsula
    ('/add', AddCapsule ), # aggiunge una capsula
    ('/cron', Cron ) # invia capsule ad utenti registrati
], debug=True )
