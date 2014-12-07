# -*- coding: latin-1 -*-

#	 This file is part of Timespace Capsule.
#
#	 Timespace Capsule is free software: you can redistribute it and/or modify
#	 it under the terms of the GNU General Public License as published by
#	 the Free Software Foundation, either version 3 of the License, or
#	 (at your option) any later version.
#
#	 Timespace Capsule is distributed in the hope that it will be useful,
#	 but WITHOUT ANY WARRANTY; without even the implied warranty of
#	 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	 GNU General Public License for more details.
#
#	 You should have received a copy of the GNU General Public License
#	 along with Timespace Capsule.  If not, see <http://www.gnu.org/licenses/>.
#
#	 Alessio Palma / 2014
#	 fb.com/alessio.palma
#	 https://sites.google.com/site/ozw1z5rd/


from google.appengine.ext import db
from datetime import datetime
from logger import L
from endpointsMessage import TSCSingleEntryResponseMessage
import math
from config import POSITION_DEFAULT_TLL

# Una capsula viene acquisita da un utente nel momento in cui
# apre il link associato.
# GAE è in UTC

class TimespaceCapsule(db.Model):

	TSC_TOOLATE = -1
	TSC_TOOSOON = -2
	TSC_TOODISTANT = -3
	TSC_BADUSER  = -4
	TSC_NOTASSIGNED = -5
	TSC_LATLNG = -6
	TSC_ENCRIPTED = -7
	TSC_OK = 1


	MESSAGE={
		TSC_TOOLATE : 'Too late, capsule expired',\
		TSC_TOOSOON : 'Too soon, capsule not yet ready',\
		TSC_TOODISTANT : 'Too distant from location',
		TSC_BADUSER : 'Registered user is not you',
		TSC_NOTASSIGNED : 'Capsule not yet assigned',
		TSC_LATLNG : 'Missing the lat lng parameter',
		TSC_ENCRIPTED : 'Content is encrypted and no password is provided'
	}

	TSC_TIMEFORMAT = "%d-%m-%Y"

	# capsule creator
	owner		 = db.UserProperty()
	# user assigned, if not anonymous otherwise is the user who opened this capsule ? 
	user		 = db.UserProperty()
	# TODO : to be removed
	password	 = db.StringProperty() # 
	# time constraint
	openingDate  = db.DateTimeProperty() # don't open before
	closingDate  = db.DateTimeProperty() # don't open after
	# does anonymous can open this ?
	anonymous	= db.BooleanProperty(default=True)
	# is this content encrypted ?
	encrypt	  = db.BooleanProperty(default=False)
	# content
	content	  = db.TextProperty()
	# required by cron, each day it will check for available TSC and sends 
	# email to registered owner
	notifyDate   = db.DateTimeProperty()
	notified	 = db.BooleanProperty(default=False)
	# when the open request worked correctly
	lastSeenDate = db.DateTimeProperty()
	seen		 = db.BooleanProperty(default=False)
	# space constraint
	positionLat  = db.FloatProperty()
	positionLng  = db.FloatProperty()
	# tollerance the ownwer like
	positionTll  = db.IntegerProperty( default = POSITION_DEFAULT_TLL )

	class Response(object):
		"""
		Simple response object 
		"""
		code = TimespaceCapsule.TSC_OK;
		description = ''
		data = ''
		def __init__(self, code, description='', data=''):
			self.code = code
			self.description = description
			self.data = data


	def toEndPointMessage(self):
		"""
		Converts this entity to endpoint message ( single entry )
		"""
		return \
			TSCSingleEntryResponseMessage( 
				TSCid = self.TSCid,\
				lat = self.positionLat,\
				lng = self.positionLng,\
				tll = self.positionTll,\
				encrypted = self.encrypt,\
				anonymous = self.anonymous,\
				openingDate = self.openingDate,\
				closingDate = self.closingDate,\
				notifyDate = self.notifyDate,\
				notified = self.notified,\
				user = self.user
			)

	def notifiedDateAsString(self):
		return self.notifiedDate.strftime(TimespaceCapsule.TSC_TIMEFORMAT)

	def openingDateAsString(self):
		return self.openingDate.strftime(TimespaceCapsule.TSC_TIMEFORMAT)

	def closingDateAsString(self):
		return self.closingDate.strftime( TimespaceCapsule.TSC_TIMEFORMAT)

	def assignToUser(self, user):
		self.user = user
		self.put()

	def setNotified(self):
		self.notifyDate = datetime.now()
		self.put()

	def disclose(self, lat=None, lng=None, user=None, password=None ):
		"""
		returns the content and the TSC as seen if opening condition are 
		correct.
		"""
		content = None
		rc = self._requestToOpen(user, lat, lng) 
		if rc  == TimespaceCapsule.TSC_OK:
			if self.encrypt:
				if password is None:
					return TimespaceCapsule.Response(
						code = TimespaceCapsule.TSC_ENCRIPTED
					)
				else:
					content = self.deCrypt(password)
			else:
				content = self.content

			response = TimespaceCapsule.Response(
				code = TimespaceCapsule.TSC_OK,
				data = content
			)
			self.seen = True
			self.lastSeenDate = datetime.now()
			self.put()
		else:
			response = TimespaceCapsule.Response(
				code = rc
			)
			return response;


	def distance(self, lat, lng):
		return self._distVincenty(lat, lng)

	@staticmethod
	def getCapsuleListForUser( user):
		L.info("Getting TSC list for user {0}".format(* user.get_email()))
		return TimespaceCapsule.all().filter("owner =",user )

	@staticmethod
	def getList( 
			user=None,\
			seenFlag=False,\
			assignedFlag=False,\
			notifiedFlag=False,\
			anonymous=True,\
			encryptFlag=False ):
		"""
		Return a list of TCS
		"""
		tscList1 =  \
			TimespaceCapsule.all()\
				.filter("owner =", user)\
				.filter("encrypt",encryptFlag)\
				.filter("anonymous", anonymous)\
				.filter("notified", notifiedFlag )\
				.filter("seen", seenFlag)
		if assignedFlag :
			tscList1 = tscList1.filter( "user !=", None)
		return tscList1

	@staticmethod
	def getByTSCid(tscid):
		return TimespaceCapsule.get_by_id(tscid)

	@property
	def TSCid(self):
		return self.key().id()


	def put(self, *args, **dic):
		"""Store the TSC and before that does check, raise exception if something 
		is not correct.
		Failure reasons are
		1) closingDate < openingDate 
		2) encripted flag set and no password provided
		3) empty content """
	
		L.info("Storing the TSC")
		L.info("Dumping the anonymous " + str( self.anonymous ))
		L.info("Dumping the content " + str( self.content ))
		if self.encrypt and self.password is not None and len(self.password)==0:
			raise Exception("Can't store an encripted TSC with no password")
		if self.closingDate < self.openingDate: 
			raise Exception("closing date is before the opening date ")
		if len( self.content ) == 0:
			raise Exception("empty content ")
		
		return super( TimespaceCapsule, self).put(*args, **dic)
	
	def crypt(self, key):
		"""
		Encrypt the payload using the provided key
		"""
		self.content = self.content

		pass

	def deCrypt(self, key):
		"""
		Decrypt the payload using the provided key
		"""
		return self.content

	def _requestToOpen(self, user, lat, lng ):
		"""
		Return ok if anything is fine, 
		=> the user who is opening the TSC but be the correct one
		=> if geolocalized, user position but be within tollerance values
		"""
		now = datetime.now()

		if not self.anonymous:
			if user != self.user and self.user is not None:
				return TimespaceCapsule.TSC_BADUSER
		if self.openingDate > now:
			return TimespaceCapsule.TSC_TOOSOON
		if self.closingDate is not None:
			if self.closingDate < now:
				return TimespaceCapsule.TSC_TOOLATE
		if self.positionLat is not None and self.positionLng is not None:
			if lat is None or lng is None:
				return TimespaceCapsule.TSC_LATLNG
			if self._distVincenty( lat, lng ) > self.positionTll:
				return TimespaceCapsule.TSC_TOODISTANT
		return TimespaceCapsule.TSC_OK

	def _distVincenty(self, lat1, lon1) :
		"""
		Return distance in meters beteewn 2 points.
		"""
		lat2 = self.positionLat
		lon2 = self.positionLng
		a = 6378137
		b = 6356752.3142
		f = 1/298.257223563  # WGS-84 ellipsiod

		L0 = math.radians(lon2-lon1)
		U1 = math.atan( (1-f) * math.tan(math.radians(lat1)) )
		U2 = math.atan( (1-f) * math.tan(math.radians(lat2)) )
		sinU1 = math.sin(U1)
		cosU1 = math.cos(U1)
		sinU2 = math.sin(U2)
		cosU2 = math.cos(U2)

		lambda1 = L0
		lambdaP = 0
		iterLimit = 100

		while True:
			L.info(iterLimit)
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
				cos2SigmaM = 0 # equatorial line: cosSqAlpha=0 (§6)
			C = f/16*cosSqAlpha*(4+f*(4-3*cosSqAlpha))
			lambdaP = lambda1
			lambda1 = L0 + (1-C) * f * sinAlpha *\
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
