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

#
# / -> scarica l'applicazione
# /add/ -> accetta la creazione di una nuova tsc
# /show -> mostra lo stato di una tsc
# /list -> mostra una lista di tutte le tsc
# /activate/<id> -> tenta l'apertura/attivazione di una tsc
# /radar 
#

import webapp2
from TimespaceCapsule import TimespaceCapsule
from datetime import datetime
from google.appengine.api import mail
import logging


class Home(webapp2.RequestHandler):
    """
    User home 
        lista le TSC che ha creato con il corrispettivo stato 
        permette di aggiungere o revocare le TSC
    """

    def get(self):
        return self.response.write('sei nella home')


class Cron(webapp2.RequestHandler):
    """
    Gestisce il cron per l'invio dei messaggi
    """
    def _sendMail(self, capsule):
        body="You Got A Message From Past click to open  "
        if capsule.positionLat is not None and capsule.positionLng is not None:
            body += "http://timespacecapsule.appspot.com/activate?TSCid={1}&lat=0&lan=0"\
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
                if capsule.closingDate is not None and \
                   capsule.closingDate > datetime.now():
                    if capsule.notifyDate is None:
                        if capsule.user is not None:
                            self._sendMail( capsule )
        return self.response.write("")



app = webapp2.WSGIApplication([
    ('/', Home),
    ('/cron', Cron )
], debug=True )
