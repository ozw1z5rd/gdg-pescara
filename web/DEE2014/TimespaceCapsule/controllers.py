# -*- coding: latin-1 -*-
from TimespaceCapsule import TimespaceCapsule
from logger import L
#from utilities import sendEmail


# ( rc, valore ) 
# 
# rc ==> determina se si tratta di un successo o meno e corrisponde dai codici 
# presenti in questa class
# il valore dipende dal metodo che stato chiamato 
#

class TSCController( object ):
	"""
	TSC Controller
	Knows how to use TSC depending on the context
	"""

	TSCCTRL_OK = 1
	TSCCTRL_KO = -1
	TSCCTRL_BADTSCID = -2 
	TSCCTRL_BADUSER = -3
	TSCCTRL_ASSIGNED = 2 
	
	@staticmethod
	def addCapsule(
			openingDate=None,
			closingDate=None,
			lat=None,
			lng=None,
			tll=0, 
			anonymous=True, 
			encrypt=False, 
			user=None,
			content=None,
			password=None
		):
		"""
		Add a new capsule
		Create a new capsule and assign it to current user ( owner )
		content is uniencoded
		in : all the defining capsule parameters
		out : TSCid if ok, None otherwise
		"""
		L.info("addCapsule called")
		L.debug({
			'openingDate' : openingDate, 
			'closingDate' : closingDate, 
			'lat' : lat,
			'lng' : lng, 
			'ttl' : tll,
			'anonymous' : anonymous,
			'encrypt' : encrypt,
			'user' : user,
			'content' : content, 
			'pwd len' : len(password) if password is not None else -1
		})
		try:
			tsc = \
				TimespaceCapsule(
					openingDate = openingDate,
					closingDate = closingDate,
					content = content,
					positionLat = lat,
					positionLng = lng,
					positionTll = tll,
					anonymous = anonymous,
					owner = user,
					encrypt = encrypt,
					password = password 
				)
			tsc.put()
		except Exception as e:
			L.warning("Got exception!")
			L.exception(e)
			return None
		else:
			L.info("Capsule created")
			return tsc.TSCid


	@staticmethod
	def searchCapsule(
			TSCid=None,
			seen=False,
			anonymous=True,
			notified=False,
			assigned=False,
			encrypt=False,
			user=None
		):
		"""
		Search a TSC depending on the given parameters, if tscid is 
		provided extra parameters are ignored.
		"""
		L.info("searchCapsule called ")
		L.debug({
			'Dumping paramters' : '',
			'anonymous' : anonymous, 
			'notified' : notified, 
			'assigned' : assigned, 
			'encrypt' : encrypt, 
			'user' : user 
		})
		
		# if TSCid is provided SEARCH only by TSCid.
		if TSCid is not None:
			L.info("TSCid is not None")
			tsc = TimespaceCapsule.getByTSCid( TSCid )
			tscList = [tsc] if tsc is not None else [] 
		else:
			# more elements
			tscList = TimespaceCapsule.getList( 
						user=user, 
						seenFlag=seen,
						assignedFlag=assigned,
						notifiedFlag=notified,
						encryptFlag=encrypt
					)
			
		items = [ tsc.toEndPointMessage() for tsc in tscList ]
		if any(items): 
			L.info( "No capsule found!")
		return ( TSCController.TSCCTRL_OK, items )


	@staticmethod
	def openCapsule(
			TSCid=None,
			lat=None,
			lng=None,
			password=None,
			user=None
		):
		"""
		openCapsule will assign the capsule is mode is not anonymous 
		and then will return to caller
		Is capsule is anonymous or already assigned, it will try to open it
		"""
		L.info("openCapsule Called")
		L.debug({
			'dumping parameters': '',
			'TSCid' : TSCid, 
			'lat' : lat,
			'lng' : lng, 
			'pwd len': len(password) if password is not None else -1,
			'user':user
		})
		# capsule not found
		tsc = TimespaceCapsule.getByTSCid(TSCid)
		if tsc is None:
			return (TSCController.TSCCTRL_BADTSCID, None)
		# if not anonymous here we require a valid user.
		if not tsc.anonymous and tsc.user is None:
			if user is None:
				return (TSCController.TSCCTRL_BADUSER, None)
			L.info("TSC is not anonymous, binding ...")
			L.info(user)
			tsc.assignToUser( user )
			return  (TSCController.TSCCTRL_ASSIGNED, None )
		
		# try to open
		L.info("try to disclose")
		response = tsc.disclose( 
						lat=lat,
						lng=lng,
						user=user,
						password=password
					)
		return ( TSCController.TSCCTRL_OK, response)


	@staticmethod
	def radar( TSCid=None, lat=None, lng=None):
		"""
		Return how meters are we far away the capsule.
		"""
		L.info("radar Called")
		L.debug({
			'TSCid':TSCid, 
			'lat': lat, 
			'lng':lng
		})
		tsc = TimespaceCapsule.getByTSCid(TSCid)
		if tsc is None:
			return  (TSCController.TSCCTRL_BADTSCID, None)
		return (TSCController.TSCCTRL_OK, tsc.distance( lat, lng ))
