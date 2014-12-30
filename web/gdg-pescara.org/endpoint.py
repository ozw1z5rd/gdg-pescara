# -*- coding: latin-1 -*-
import endpoints
from protorpc import remote
from endpointMessages import GDGPEPostRequest, GDGPEPostResponse

@endpoints.api(name="gdgPescaraOrg", version="v1", description="GDG Pescara endpoints", hostname ="localhost")
class GDGPEEndpoint(remote.Service):
	
	@endpoints.method(GDGPEPostRequest,GDGPEPostResponse,name="gdgPE.getPostList",http_method="POST")
	def getPostList(self,request):
		author = request.author
		dateStart = request.dateStart
		ID = request.id
		sector = request.sector
		tags = request.tags
		
		return author + dateStart + ID + sector + tags

# see application.yaml
APPLICATION=endpoints.api_server([GDGPEEndpoint], restricted=False)
