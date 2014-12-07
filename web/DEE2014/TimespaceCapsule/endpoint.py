# -*- coding: latin-1 -*-
import endpoints
from protorpc import remote
from endpointsMessage import TSCRequesAddtMessage
from endpointsMessage import TSCRequestOpenMessage
from endpointsMessage import TSCRequestRadarMessage
from endpointsMessage import TSCResponseMessage
from endpointsMessage import TSCRequestSearchMessage
from TimespaceCapsule import TimespaceCapsule
from controllers import TSCController
from logger import L

@endpoints.api(name="timeSpaceCapsule", version="v1", description="TSC endpoint", hostname ="localhost")
class TSCEndpoint( remote.Service ):
	"""TSC endpoints class.
	"""

	@staticmethod
	def get_current_user(raiseException = False):
		"""Find the current user, if any.
		No user => return None if raiseException is False, otherwise
		exception :-)
		"""
		user = endpoints.get_current_user()
		if raiseException and user is None:
			raise endpoints.UnauthorizedException('Invalid token')
		return user


	@endpoints.method(TSCRequesAddtMessage, TSCResponseMessage, \
					  name="TSC.add", http_method="POST" )
	def addCapsule(self, request):
		"""add a new capsule, edit and delete is not allowed
		"""
		# probabilmente ci deve essere un sistema migliore di fare
		# questo passaggio dei parametri
		openingDate = request.openingDate
		closingDate = request.closingDate
		lat = request.lat
		lng = request.lng
		tll = request.tll
		anonymous = request.anonymous
		encrypt = request.encrypted
		content = request.content

		user =  TSCEndpoint.get_current_user()
		TSCid = TSCController.addCapsule(openingDate, closingDate, \
			lat, lng, tll, anonymous, encrypt, user, content)
		if TSCid is None:
			response = TSCResponseMessage(
				TSCid = None,
				status = TSCController.TSCCTRL_KO,
				statusMessage = 'Capsule not created.',
				content = '',
				items = [] )
		else:
			L.info("Capsule created")
			response = TSCResponseMessage(
				TSCid = TSCid,
				status = TSCController.TSCCTRL_OK,
				statusMessage = 'Capsule correctly created',
				content = '',
				items = [] )

		return response


	@endpoints.method(TSCRequestOpenMessage, TSCResponseMessage, \
					  name="TSC.open", http_method="POST" )

	def openCapsule(self, request):
		"""request to open the capsule,
		if capsule is not for anonymous on first run will be assigned to
		the user and only the owener can request the opening
		"""
		TSCid = request.TSCid
		user = TSCEndpoint.get_current_user()

		( rc, response ) = TSCController.openCapsule(TSCid, request.lat, request.lng, request.password, user)
		# assign the capsule if not anonymous and not yet assigned
		if rc == TSCController.TSCCTRL_BADTSCID:
			raise endpoints.NotFoundException('Bad tscid!')
		elif rc == TSCController.TSCCTRL_BADUSER:
				raise endpoints.BadRequestException("Can't find a user")
		elif rc == TSCController.TSCCTRL_ASSIGNED:
			return TSCResponseMessage(
				TSCid = TSCid,
				status = TSCController.TSCCTRL_OK,
				statusMessage = 'Assigned!',
				content = '',
				items = [] )
		# anything which does not fit into the above cases
		elif rc != TSCController.TSCCTRL_OK:
			return TSCResponseMessage(
				TSCid = TSCid,
				status = rc,
				statusMessage = 'TSCController rc',
				content = '',
				items = [] )

		return TSCResponseMessage(
			TSCid = TSCid,
			status = TSCController.TSCCTRL_KO
				if response.code != TimespaceCapsule.TSC_OK
				else TSCController.TSCCTRL_OK,
			statusMessage = "disclose code: "+ TimespaceCapsule.MESSAGE[response.code],
			content = response.data,
			items = [] )



	@endpoints.method(TSCRequestRadarMessage, TSCResponseMessage, \
					  name="TSC.radar", path="TSC", http_method="POST" )
	def radar(self, request):
		"""target distance.
		say how far is the device from the TSC.
		It's not a good idea keep querying the server.
		Very few logic, can stay here.
		"""
		TSCid = request.TSCid
		#tsc = TimespaceCapsule.getByTSCid(TSCid)

		( rc, distance ) = TSCController.radar(TSCid, request.lat, request.lng)

		if rc == TSCController.TSCCTRL_OK:
			return TSCResponseMessage(
				TSCid = TSCid,
				status = TSCController.TSCCTRL_KO,
				content = str( distance ),
				items = [] )

		return TSCResponseMessage(
			TSCid = TSCid,
			status = TSCController.TSCCTRL_KO,
			items = [] )



	@endpoints.method(TSCRequestSearchMessage, TSCResponseMessage, \
					  name="TSC.search", path="TSC", http_method='GET' )

	def listCapsule(self, request):
		"""list capsule depending on search parameters
		This will be the most used api
		"""
		user = TSCEndpoint.get_current_user()

		( rc, items ) = TSCController.searchCapsule(
				TSCid = request.TSCid, \
				seen = request.seen, \
				anonymous = request.anonymous, \
				encrypt=request.encrypt, \
				user = user)

		L.info("Logging degli items")
		L.info(items)
		if not rc == TSCController.TSCCTRL_OK :
			raise endpoints.InternalServerErrorException("Something goes bad")
		return TSCResponseMessage( TSCid = None, status = TSCController.TSCCTRL_OK, \
			statusMessage = '', items = items )



# see application.yaml
APPLICATION=endpoints.api_server([TSCEndpoint], restricted=False)
