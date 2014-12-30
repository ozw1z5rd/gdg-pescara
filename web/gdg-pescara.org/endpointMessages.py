# -*- coding: latin-1 -*-
from protorpc import messages, message_types

class GDGPETagSingle(messages.Message):
	tag = messages.StringField(1)

# ----
#
# REQUEST ---------------- Parametri da passare nelle chiamate
#
# lo user e' implicito e può essere risolto con una chiamata alle api di G.
# direttamente nel codice di BE.
#
# tutte le chiamate curd ottengono in risposta l'ID dell'oggetto creato
#

class GDGPEPostRequest(messages.Message):
	"""Richiesta per avere i dati di uno o piu' post"""
	author = messages.StringField(1,required=False)
	dateStart = message_types.DateTimeField(2,required=False)
	dateEnd = message_types.DateTimeField(3,required=False)
	id = messages.StringField(4,required=False)
	sector = messages.StringField(5,required=False)
	tags = messages.MessageField(GDGPETagSingle,6,repeated=True)

class GDGPEQuizRequest(messages.Message):
	"""Richiesta per avere il Quiz corrente"""
	dateNow = message_types.DateTimeField(1,required=True)
	
class GDGPEQuizUpdateRequest(messages.Message):
	"""Richiesta di aggiornamento della risposta al quiz, aggiorna il 
	contatore delle risposte e mostra la risposta corretta all'utente"""
	dateNow = message_types.DateTimeField(2,required=True)
	answerId = messages.IntegerField(3, required=True)
	
class GDGPEQuestionCreateRequest(messages.Message):
	"""Crea una domanda"""
	body = messages.StringField(2,required=True)
	tags = messages.StringField(3, required=False) #CSV
	sector = messages.StringField(4,required=True)
	
class GDGPEQuestionAnswerRequest(messages.Message):
	"""Risponde ad una domanda"""
	questionId = messages.StringField(1, required=True)
	body = messages.StringField(2,required=True)
	dateNow = messages.StringField(3,required=True)
	
class GDGPEQuestionAnswerReplyRequest(messages.Message):
	"""Aggiunge un commento ad una risposta data ad una domanda"""
	answerId = messages.StringField(1,required=True)
	body = messages.StringField(2,required=True)
	dateNow = message_types.DateTimeField(3,required=False)

# ----
#
# RESPONSES -------------- Quello che l'endpoint torna al chiamante
#

# ---- "mattoni" base per le risposte che prevedono più ripetizioni 
#      di strutture dati ( solo per risposte )

class GDGPELinkSingleResponse(messages.Message):
	url = messages.StringField(1)
	id = messages.StringField(2)

class GDGPETechnologySingleResponse(messages.Message):
	description = messages.StringField(1)
	iconLink = messages.StringField(2)
	id = messages.StringField(3)

class GDGPEAuthorSingleResponse(messages.Message):
	nickName = messages.StringField(1)
	technologies = messages.MessageField(GDGPETechnologySingleResponse,2,repeated=True)

class GDGPESectorSingleResponse(messages.Message):
	title = messages.StringField(1)
	description = messages.StringField(2)
	id = messages.StringField(3)

class GDGPEQuizsAnswerSingleResponse(messages.Message):
	body = messages.StringField(1)
	click = messages.IntegerField(2)
	index = messages.IntegerField(3)
	isCorrect = messages.BooleanField(4,default=False)
	id = messages.StringField(5)

class GDGPEQuestionsAnswerSingleResponse(messages.Message):
	body = messages.StringField(2)
	rating = messages.IntegerField(3)
	id = messages.StringField(4)
	relatedTo = messages.IntegerField(5,required=True)
	
# ---- 
# Queste che seguono sono le risposte "di uso comune e di alto livello
#
class GDGPETecnologyListResponse(messages.Message):
	technologies = messages.MessageField(GDGPETechnologySingleResponse,1,repeated=True)

# ---- quiz 

# Get a post ( single )
class GDGPEPostResponse(messages.Message):
	title = messages.StringField(1)
	tags = messages.MessageField(GDGPETagSingle,2) 
	date = message_types.DateTimeField(3)
	imageLink = messages.StringField(4)
	body = messages.StringField(5)
	author= messages.MessageField(GDGPEAuthorSingleResponse,6)
	repositoryLink = messages.StringField(7)
	reference = messages.MessageField(GDGPELinkSingleResponse,8,repeated=True)
	sector = messages.MessageField(GDGPESectorSingleResponse,9,repeated=True)
	id = messages.StringField(10)
	
# Get today quiz
class GDGPEQuizResponse(messages.Message):
	title = messages.StringField(1)
	body = messages.StringField(2)
	answers = messages.MessageField( GDGPEQuizsAnswerSingleResponse, 3, repeated=True)
	id = messages.StringField(4)

# ---- Question 
class GDGPEAnswerResponse(messages.Message):
	body = messages.StringField(1)
	tags = messages.MessageField(GDGPETagSingle,2)
	answers = messages.MessageField(GDGPEQuestionsAnswerSingleResponse,3,repeated=True)
	id = messages.StringField(4)