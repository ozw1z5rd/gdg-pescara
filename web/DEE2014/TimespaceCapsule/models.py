# -*- coding: latin-1 -*-

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


from google.appengine.ext import db
from datetime import datetime
import math

# Una capsula viene acquisita da un utente nel momento in cui
# apre il link associato.
# GAE � in UTC

class TimespaceCapsule(db.Model):

    TSC_TOOLATE = -1
    TSC_TOOSOON = -2
    TSC_TOODISTANT = -3
    TSC_BADUSER  = -4
    TSC_NOTASSIGNED = -5
    TSC_LATLNG = -6
    TSC_OK = 1

    user        = db.UserProperty()       # owner

    openingDate = db.DateTimeProperty()   #don't open before
    closingDate = db.DateTimeProperty()   #don't read after
    notifyDate  = db.DateTimeProperty()   #usually the same as openingDate
    anonymous   = db.BooleanProperty()    #allow anonymous to open it

    content     = db.TextProperty()       #payload
    seen         = db.BooleanProperty()   #seen
    lastSeenDate = db.DateTimeProperty()  #if seen

    positionLat = db.FloatProperty()      #open at location
    positionLng = db.FloatProperty()
    positionTll = db.FloatProperty()

    def assignToUser(self, user):
        self.user = user
        self.put()

    def setNotified(self):
        self.notifyDate = datetime.now()
        self.put()

    def show(self):
        """
        Torna il contenuto e setta la capsula come vista
        """
        self.seen = True
        self.lastSeenDate = datetime.now()
        self.put()
        return self.content

    def requestToOpen(self, user, lat, lng ):
        """
        Torna OK se tutti i parametri sono validi
        se non c'� un utente al momento dell'apertura pu� essere aperta
        da chiunque
        """
        now = datetime.now()

        if not self.anonymous:
            if user != self.user and self.user is not None:
                return self.TSC_BADUSER
        if self.openingDate > now:
            return self.TSC_TOOSOON
        if self.closingDate is not None:
            if self.closingDate < now:
                return self.TSC_TOOLATE
        if self.positionLat is not None and self.positionLng is not None:
            if lat is None or lng is None:
                return self.TSC_LATLNG
            if self._distVincenty( lat, lng ) > self.positionTll:
                return self.TSC_TOODISTANT

        return self.TSC_OK

    def _distVincenty(self, lat1, lon1) :
        """
        Distanza tra due punti sul nostro deforme mondo, il valore
        tornato � in metri, le due posizioni devono essere passate in
        gradi
        """
        lat2 = self.positionLat
        lon2 = self.positionLng
        a = 6378137
        b = 6356752.3142
        f = 1/298.257223563  # WGS-84 ellipsiod

        L = math.radians(lon2-lon1)
        U1 = math.atan( (1-f) * math.tan(math.radians(lat1)) )
        U2 = math.atan( (1-f) * math.tan(math.radians(lat2)) )
        sinU1 = math.sin(U1)
        cosU1 = math.cos(U1)
        sinU2 = math.sin(U2)
        cosU2 = math.cos(U2)

        lambda1 = L
        lambdaP = 0
        iterLimit = 100

        while True:
            sinLambda = math.sin(lambda1)
            cosLambda = math.cos(lambda1)
            sinSigma = math.sqrt((cosU2*sinLambda)
                       * (cosU2*sinLambda)
                       + (cosU1*sinU2-sinU1*cosU2*cosLambda)
                       * (cosU1*sinU2-sinU1*cosU2*cosLambda))
            if sinSigma==0 :
                return 0
            try:
                cosSigma = sinU1*sinU2 + cosU1*cosU2*cosLambda
                sigma = math.atan2(sinSigma, cosSigma)
                sinAlpha = cosU1 * cosU2 * sinLambda / sinSigma
                cosSqAlpha = 1 - sinAlpha*sinAlpha
                cos2SigmaM = cosSigma - 2*sinU1*sinU2/cosSqAlpha
            except:
                cos2SigmaM = 0 # equatorial line: cosSqAlpha=0 (�6)
            C = f/16*cosSqAlpha*(4+f*(4-3*cosSqAlpha))
            lambdaP = lambda1
            lambda1 = L + (1-C) * f * sinAlpha *\
                (sigma + C*sinSigma*(cos2SigmaM+C*cosSigma*\
                (-1+2*cos2SigmaM*cos2SigmaM)))

            iterLimit = iterLimit - 1
            if abs(lambda1-lambdaP) > 1e-12 and iterLimit>0 :
                break
        if iterLimit==0 :
            return None # formula failed to converge
        uSq = cosSqAlpha * (a*a - b*b) / (b*b)
        A = 1 + uSq/16384*(4096+uSq*(-768+uSq*(320-175*uSq)))
        B = uSq/1024 * (256+uSq*(-128+uSq*(74-47*uSq)))
        deltaSigma = B*sinSigma*(cos2SigmaM+B/4*(cosSigma*
                     (-1+2*cos2SigmaM*cos2SigmaM)-
                     B/6*cos2SigmaM*(-3+4*sinSigma*sinSigma)*
                     (-3+4*cos2SigmaM*cos2SigmaM)))
        s = b*A*(sigma-deltaSigma);
        return s
