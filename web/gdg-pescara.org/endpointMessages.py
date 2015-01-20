# -*- coding: latin-1 -*-\
from protorpc import messages, message_types

# ----
# Elementi che compongono risposte strutturate ma che di conto proprio non 
# sono rappresentativi.
#
class GDGPETagElement(messages.Message):
	tag = messages.StringField(1)

class GDGPEImageElement(messages.Message):
	data = messages.BytesField(1,required=True)

class GDGPELinkElement(messages.Message):
	url = messages.StringField(1,required=True)
	
class GDGPEStringElement(messages.Message):
	value = messages.StringField(1,required=True)
	
class GDGPEMetaDataElement(messages.Message):
	"""Tutte le risposte hanno questo preambolo che permette di gestire redirect
	errori a livello di logica etc..."""
	status = messages.StringField(1,required=True)
	code = messages.IntegerField(2,required=True)
	redirectUrl = messages.StringField(3,required=True)
	# campi addizionali per debug
	debug1 = messages.StringField(4, required=False)
	debug2 = messages.BytesField(5,required=False)
	

class GDGPESectorElement(messages.Message):
	title = messages.StringField(1)
	description = messages.StringField(2)
	id = messages.StringField(3)

class GDGPETechnologyElement(messages.Message):
	description = messages.StringField(1)
	iconLink = messages.StringField(2)
	id = messages.StringField(3)

class GDGPEAuthorElement(messages.Message):
	nickName = messages.StringField(1)
	technologies = messages.MessageField(GDGPETechnologyElement,2,repeated=True)

class GDGPEQuestionsAnswerElement(messages.Message):
	body = messages.StringField(2)
	rating = messages.IntegerField(3)
	id = messages.StringField(4)
	relatedTo = messages.IntegerField(5,required=True)

class GDGPEQuizsAnswerElement(messages.Message):
	body = messages.StringField(1)
	click = messages.IntegerField(2)
	index = messages.IntegerField(3)
	isCorrect = messages.BooleanField(4,default=False)
	id = messages.StringField(5)

# ----
#
# REQUEST ---------------- Parametri da passare nelle chiamate
#
# lo user e' implicito e può essere risolto con una chiamata alle api di G.
# direttamente nel codice di BE.
#
# tutte le chiamate curd ottengono in risposta l'ID dell'oggetto creato
#
class GDGPEEmptyRequest(messages.Message):
	"""Non tutte le api necessitano di parametri"""
	pass

class GDGPEPostRequest(messages.Message):
	"""Richiesta per avere i dati di uno o piu' post. I parametri saranno usati
	per eseguire una "SELECT" sul datastore."""
	author = messages.StringField(1,required=False)
	dateStart = message_types.DateTimeField(2,required=False)
	dateEnd = message_types.DateTimeField(3,required=False)
	id = messages.StringField(4,required=False)
	sector = messages.StringField(5,required=False)
	tags = messages.MessageField(GDGPETagElement,6,repeated=True)

class GDGPEQuizRequest(messages.Message):
	"""Richiesta per avere il Quiz valido nella dta indicata"""
	dateNow = message_types.DateTimeField(1,required=True)
	
class GDGPEQuizUpdateRequest(messages.Message):
	"""Richiesta di aggiornamento della risposta al quiz, aggiorna il 
	contatore delle risposte e mostra la risposta corretta all'utente"""
	dateNow = message_types.DateTimeField(2,required=True)
	# indica la risposta che secondo l'utente è valida.
	answerId = messages.IntegerField(3, required=True)
	
class GDGPEQuestionCreateRequest(messages.Message):
	"""Crea una domanda"""
	body = messages.StringField(2,required=True)
	tags = messages.MessageField(GDGPETagElement,3,repeated=True)
	sector = messages.StringField(4,required=True)
	
class GDGPEQuestionAnswerRequest(messages.Message):
	"""Risponde ad una domanda"""
	questionId = messages.StringField(1, required=True)
	body = messages.StringField(2,required=True)
	dateNow = messages.StringField(3,required=True)
	
class GDGPEQuestionAnswerReplyRequest(messages.Message):
	"""Aggiunge un commento ad una risposta assegnata ad una domanda"""
	answerId = messages.StringField(1,required=True)
	body = messages.StringField(2,required=True)
	dateNow = message_types.DateTimeField(3,required=False)

class GDGPECreatePostRequest(messages.Message):
	"""Creazione di un nuovo post."""
	title = messages.StringField(1,required=True)
	tags = messages.MessageField(GDGPETagElement,2,repeated=True)
	sector = messages.StringField(3,required=True)
	date = message_types.DateTimeField(4,required=True)
	image = messages.MessageField(GDGPEImageElement,5,repeated=True)
	body = messages.StringField(6,required=True)
	authors = messages.MessageField( GDGPEStringElement,7,repeated=True)
	repositoryLink = messages.MessageField( GDGPELinkElement,8,repeated=True)
	reference = messages.MessageField( GDGPELinkElement,9,repeated=True)
	messages.BytesField

class GDGPESubscribeUserRequest(messages.Message):
	"""Questa chiamata dovrebbe funzionare sull'utente attualmente 
	loggato, l'email serve quando viene chiamata dall'utente amministratore"""
	email = messages.StringField(1,required=False)

class GDGPEUnsubscribeUserRequest(messages.Message):
	"""Questa chiamata dovrebbe funzionare sull'utente attualmente 
	loggato, l'email serve quando viene chiamata dall'utente amministatore"""
	email = messages.StringField(1,required=False)

class GDGPEUserInfoRequest(messages.Message):
	"""Questa chiamata dovrebbe funzionare sull'utente attualmente 
	loggato, l'email serve quando viene chiamata dall'utente ammininistratore"""	
	email = messages.StringField(1,required=False)

class GDGPEChangeUserInfoRequest(messages.Message):
	"""cambia le impostazioni dell'utente"""
	allowsMailing = messages.BooleanField(1,required=True)

class GDGPEQuestionAnswerRatingRequest(messages.Message):
	"""Serve a dare un punteggio ad una risposta assegnata ad una domanda"""
	id = messages.StringField(1,required=True)

# ----
#
# RESPONSES -------------- Quello che l'endpoint torna al chiamante
#

# ---- "mattoni" base per le risposte che prevedono più ripetizioni 
#      di strutture dati ( solo per risposte )



class GDGPEEmptyResponse(messages.Message):
	"""Risposta vuota per errori in cui non è possibile elaborare neanche 
	parzialmente la risposta"""
	meta = messages.MessageField(GDGPEMetaDataElement,1)

# ---- 
# Queste che seguono sono le risposte "di uso comune e di alto livello
#
class GDGPETecnologyListResponse(messages.Message):
	meta = messages.MessageField(GDGPEMetaDataElement,1) 
	technologies = messages.MessageField(GDGPETechnologyElement,2,repeated=True)

# ---- quiz 

# Get a post ( single )
class GDGPEPostResponse(messages.Message):
	meta = messages.MessageField(GDGPEMetaDataElement,1)
	title = messages.StringField(2)
	tags = messages.MessageField(GDGPETagElement,3) 
	date = message_types.DateTimeField(4)
	imageLink = messages.StringField(5)
	body = messages.StringField(6)
	author= messages.MessageField(GDGPEAuthorElement,7)
	repositoryLink = messages.StringField(8)
	reference = messages.MessageField(GDGPELinkElement,9,repeated=True)
	sector = messages.MessageField(GDGPESectorElement,10,repeated=True)
	id = messages.StringField(11)
	
# Get today quiz
class GDGPEQuizResponse(messages.Message):
	meta = messages.MessageField(GDGPEMetaDataElement,1)
	title = messages.StringField(2)
	body = messages.StringField(3)
	answers = messages.MessageField( GDGPEQuizsAnswerElement, 4, repeated=True)
	id = messages.StringField(5)

# ---- Question 
class GDGPEAnswerResponse(messages.Message):
	meta = messages.MessageField( GDGPEMetaDataElement,1)
	body = messages.StringField(2)
	tags = messages.MessageField(GDGPETagElement,3)
	answers = messages.MessageField(GDGPEQuestionsAnswerElement,4,repeated=True)
	id = messages.StringField(5)
	
# User

class GDGPESubscribeUserResponse(messages.Message):
	meta = messages.MessageField(GDGPEMetaDataElement,1)
	id = messages.StringField(2, required=True)
	allowsMailing = messages.BooleanField(3,required=True)

class GDGPEUnsubscribeUserResponse(messages.Message):
	"""cancella l'utente attualmente connesso con la richiesta"""
	meta = messages.MessageField(GDGPEMetaDataElement,1)

class GDGPEUserInfoResponse(messages.Message):
	meta = messages.MessageField(GDGPEMetaDataElement,1)
	
class GDGPEChangeUserInfoResponse(messages.Message):
	"""cambia le impostazioni dell'utente"""
	meta = messages.MessageField(GDGPEMetaDataElement,1)
	allowsMailing = messages.BooleanField(2,required=False)

# rating 

class GDGPEQuestionAnswerRatingResponse(messages.Message):
	meta = messages.MessageField(GDGPEMetaDataElement,1)
