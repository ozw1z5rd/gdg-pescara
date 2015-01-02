# -*- coding: latin-1 -*-
import endpoints
from protorpc import remote
from endpointMessages import GDGPEPostRequest, GDGPEPostResponse,\
	GDGPEEmptyRequest, GDGPETecnologyListResponse, GDGPEQuizRequest,\
	GDGPEQuizResponse, GDGPEQuestionCreateRequest, GDGPEAnswerResponse,\
	GDGPEQuestionAnswerRequest, GDGPEQuestionAnswerReplyRequest,\
	GDGPEQuizUpdateRequest, GDGPECreatePostRequest

@endpoints.api(name="gdgPescaraOrg", version="v1", description="GDG Pescara endpoints", hostname ="localhost")
class GDGPEEndpoint(remote.Service):

	#
	# Article
	# 
	@endpoints.method(GDGPEPostRequest,GDGPEPostResponse,name="gdgPE.getPostList",http_method="POST")
	def searchPosts(self,request):
		author = request.author
		dateStart = request.dateStart
		ID = request.id
		sector = request.sector
		tags = request.tags
		return author + dateStart + ID + sector + tags
	
	@endpoints.method(GDGPECreatePostRequest,GDGPEPostResponse,name="gdgPE.createPost",http_method="POST")
	def createPost(self,request):
		return ""
	
	#
	# Tech List
	#
	@endpoints.method(GDGPEEmptyRequest,GDGPETecnologyListResponse,name="gdgPE.getTechList",http_method="POST")
	def getTechList(self,request):
		return ""
	
	#
	# Quiz
	#
	@endpoints.method(GDGPEQuizRequest,GDGPEQuizResponse,name="gdgPE.getQuiz",http_method="POST")
	def getQuiz(self,request):
		return ""
	
	@endpoints.method(GDGPEQuizUpdateRequest,GDGPEQuizResponse,name="gdgPE.replyQuiz",http_method="POST")
	def answerQuiz(self,request):
		return ""
	
	#
	# Question
	#
	@endpoints.method(GDGPEQuestionCreateRequest,GDGPEAnswerResponse,name="gdgPE.createQuestion",http_method="POST")
	def createQuestion(self,request):
		return ""

	@endpoints.method(GDGPEQuestionAnswerRequest,GDGPEAnswerResponse, name="gdgPE.answerQuestion", http_method="POST")
	def answerQuestion(self,request):
		return ""
	
	@endpoints.method(GDGPEQuestionAnswerReplyRequest,GDGPEAnswerResponse,name="gdgPE.replyQuestionAnswer",http_method="POST")
	def replyAnswer(self,request):
		return ""
	
	
	
# see application.yaml
APPLICATION=endpoints.api_server([GDGPEEndpoint], restricted=False)





