# -*- coding: latin-1 -*-
#
# traduce richieste e risposte per endpoints
#

import endpoints
from protorpc import remote
from endpointMessages import GDGPEPostRequest, GDGPEPostResponse,\
	GDGPEEmptyRequest, GDGPETecnologyListResponse, GDGPEQuizRequest,\
	GDGPEQuizResponse, GDGPEQuestionCreateRequest, GDGPEAnswerResponse,\
	GDGPEQuestionAnswerRequest, GDGPEQuestionAnswerReplyRequest,\
	GDGPEQuizUpdateRequest, GDGPECreatePostRequest, GDGPESubscribeUserRequest,\
	GDGPEUnsubscribeUserRequest, GDGPEUserInfoRequest, GDGPEUserInfoResponse,\
	GDGPEUnsubscribeUserResponse, GDGPESubscribeUserResponse,\
	GDGPEQuestionAnswerRatingRequest, GDGPEQuestionAnswerRatingResponse,\
	GDGPEMetaDataElement

from Controller import TechnologyController
from logger import L


@endpoints.api(name="gdgPescaraOrg", version="v1", description="GDG Pescara endpoints") # hostname = "localhost" o piu' in generare il dominio che serve l'app
class GDGPEEndpoint(remote.Service):

	META_CODE_OK = 1
	META_CODE_REDIRECT = 2
	META_CODE_ERROR = -1

	#not endpoint method
	def getGDGPEMetaElementByCode(self, code, status="", url=None, d1=None, d2=None):
		return GDGPEMetaDataElement(
			status = status, 
			code = code,
			redirectUrl = url,
			debug1=d1,
			debug2=d2
		)

	#
	# Article
	# 
	@endpoints.method(GDGPEPostRequest,GDGPEPostResponse, name="gdgPE.post.getList", path="", http_method="POST")
	def searchPosts(self,request):
		author = request.author
		dateStart = request.dateStart
		ID = request.id
		sector = request.sector
		tags = request.tags
		
		L.i("Entering searchPost")
		L.i(request)
		
		return author + dateStart + ID + sector + tags
	
	@endpoints.method(GDGPECreatePostRequest,GDGPEPostResponse,name="gdgPE.post.create",http_method="POST")
	def createPost(self,request):
		L.i("Create Post Request")
		L.i(request)
		return ""
	
	#
	# Tech List
	#
	@endpoints.method(GDGPEEmptyRequest,GDGPETecnologyListResponse,name="gdgPE.tech.getList",http_method="POST")
	def getTechList(self,request):
		L.i("Entering in getTechList")
		return GDGPETecnologyListResponse(
			meta = self.getGDGPEMetaElementByCode( GDGPEEndpoint.META_CODE_OK_ ),
			technologies = list([x.asMessageElement for x in TechnologyController.getList()])
		)
	
	#
	# Quiz
	#
	@endpoints.method(GDGPEQuizRequest,GDGPEQuizResponse,name="gdgPE.quiz.get",http_method="POST")
	def getQuiz(self,request):
		L.i(request)
		return ""
	
	@endpoints.method(GDGPEQuizUpdateRequest,GDGPEQuizResponse,name="gdgPE.quiz.reply",http_method="POST")
	def answerQuiz(self,request):
		return ""
	
	#
	# Question
	#
	@endpoints.method(GDGPEQuestionCreateRequest,GDGPEAnswerResponse,name="gdgPE.question.create",http_method="POST")
	def createQuestion(self,request):
		L.i(GDGPEQuestionCreateRequest)
		return ""
	@endpoints.method(GDGPEQuestionAnswerRequest,GDGPEAnswerResponse, name="gdgPE.question.answer", http_method="POST")
	def answerQuestion(self,request):
		L.i(request)
		return ""
	
	@endpoints.method(GDGPEQuestionAnswerReplyRequest,GDGPEAnswerResponse,name="gdgPE.questionAnswer.reply",http_method="POST")
	def replyAnswer(self,request):
		L.i(request)
		return ""
	
	# permette di dare una preferenza ad una risposta.
	@endpoints.method(GDGPEQuestionAnswerRatingRequest,GDGPEQuestionAnswerRatingResponse,name="gdgPE.questionAnswer.rate",http_method="POST")
	def rateQuestionAnswer(self,request):
		L.i(request)
		return
	#
	# User
	#
	@endpoints.method(GDGPESubscribeUserRequest, GDGPESubscribeUserResponse, name="gdgPE.user.subscribe",http_method="POST")
	def subscribeUser(self,request):
		L.i(request)
		return ""
	
	@endpoints.method(GDGPEUnsubscribeUserRequest, GDGPEUnsubscribeUserResponse, name="gdgPE.user.unsubscribe",http_method="POST")
	def unsubscribeUser(self,request):
		L.i(request)
		return ""
	
	@endpoints.method(GDGPEUserInfoRequest, GDGPEUserInfoResponse, name="gdgPE.user.info", http_method="POST")
	def userInfo(self,request):
		L.i(request)
		return
	
# see application.yaml
APPLICATION=endpoints.api_server([GDGPEEndpoint], restricted=False)





