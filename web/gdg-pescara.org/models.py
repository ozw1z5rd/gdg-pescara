# -*- coding: latin-1 -*-
#
# 29/12/2014 -> prima bozza
# 09/01/2014 -> qualcosa di più corretto e stabile
# 06/02/2015 -> sostituito UserProperty con una StringPropertu in modo da 
#               tracciare solo l'id univoco dell'utente.
#
# Ogni oggetto puo' renderizzarsi in un MessageElement ( endpointMessages )
# e qualcuno può essere creato da un messaggio di endpoints
# la conversione a MessageElement deve essere fatta in modo puntuale
#
#
# Metodi comuni a tutti gli oggetti del model.
#
# newFromRequest -> un nuovo oggetto da una richiesta
# asMessageElement -> fa il cast ad MessageElement ( serve per l'impacchettamento )
# getById -> recupera l'elemento per Id 
# getAll -> torna tutti gli elementi 

from google.appengine.ext import db
from endpointMessages import GDGPETechnologyElement
from utility import blobToImageUrl
from config import DEBUG_MODE

class Link(db.Model):
	title = db.StringProperty()
	url = db.URLProperty()
	clicks = db.IntegerProperty()

class Technology(db.Model):
	"""Descrive una delle possibiliti tecnologie trattate"""
	title = db.StringProperty()
	description = db.TextProperty()
	icon = db.BlobProperty()

	def getAll(self):
		"""torna tutti gli elementi"""
		return self.all()

	def asMessageElement(self):
		return GDGPETechnologyElement( 
			id = str(self.key()),
			title = self.title,
			description = self.description, 
			iconLink = blobToImageUrl(self.icon) 
	)

class UserTechnology(db.Model):
	"""La UserTechnology serve per poter associare un rating ad una determinata
	tecnologia per un determinato utente, il calcolo viene fatto in modalita'
	batch leggendo i referrer.
	Periodicamente un cron aggiorna i rating per tecnologia sugli utenti che 
	hanno referrer da parte di altri utenti"""
	technology=db.ReferenceProperty(Technology)
	rating = db.RatingProperty()
	
class User(db.Model):
	"""Definisce un utente di questo sistema, pochi dati per non dire 
	pochissimi, l'autenticazione e' a carico di Google"""
	# rappresenta l'id dell'utente 
	# https://cloud.google.com/appengine/docs/python/users/userobjects
	user_id = db.StringProperty()
	lastLogin = db.DateTimeProperty()
	technologies = db.ListProperty(db.Key)# UserTechnology
	allowsMailing = db.BooleanProperty(default=True)
	
	# debug purposes
	__email = db.StringProperty()
	__user = db.StringProperty()
	
	def email(self):
		if DEBUG_MODE:
			return self.__email 
		return self.user.email()
	def username(self):	
		if DEBUG_MODE:
			return self.__user
		return self.user.nickname()
	
class Image(db.Model):
	"""Serve per poter memorizzare le immagini nel datastore"""
	description = db.StringProperty()
	link = db.LinkProperty()
	# MIME type
	type = db.StringProperty()
	blob = db.BlobProperty()

class Sector(db.Model):
	"""Settore di interesse, per esempio web development oppure IoT etc...
	ogni articolo viene associato ad un settore"""
	title = db.StringProperty()
	description = db.StringProperty()

class Post(db.Model):
	"""descrive un articolo, essenzialmente un articolo puo' far parte di due
	macro categorie: context( news ) e technical ( info tecniche )"""
	title = db.StringProperty()
	tags = db.ListProperty(str)
	sector = db.ListProperty(db.Key)#Sector
	date = db.DateProperty()
	image = db.ListProperty(db.Key) # Image
	body = db.TextProperty()
	authors = db.ListProperty(db.Key)#User
	repositoryLink = db.ListProperty(db.Key) # Link !!! 
	reference = db.ListProperty(db.Key) # LInk !!!
	
# periodicamnete possibile visualizzare qiz per tenere i programmatori 
# "in forma"
class QuizsAnswer(db.Model):
	"""Una delle possibili risposte del quiz"""
	text = db.StringProperty()
	isCorrect = db.BooleanProperty()
	# quanto hanno risposto
	click = db.IntegerProperty()

class Quiz(db.Model):
	"""Definisce un quiz come una domanda, un intervallo di validita' per il quiz
	stesso ed una lista di risposte ( di cui una o piu' corretta )"""
	title = db.StringProperty()
	body = db.TextProperty()
	dateStart = db.DateProperty()
	dateEnd = db.DateProperty()
	answer = db.ListProperty(db.Key)# Quizanswer                               
	# utenti che hanno gia'  risposto al quiz
	users = db.ListProperty(db.Key)#User

class Refer(db.Model):
	"""Permette agli utenti di dare referenze ad altri utenti su determinate 
	tecnologie"""
	user = db.ReferenceProperty(User)
	technology = db.ReferenceProperty(Technology,collection_name="rTechnology")
	stars = db.RatingProperty()
	who = db.ReferenceProperty(User,collection_name="rUser")
	description = db.StringProperty()
	
class QuestionAnswer(db.Model):
	"""Risposta ad una risposta da parte di un altro utente, il rating e' una 
	sorta di "like" alla facebook """
	body = db.TextProperty()
	rating = db.RatingProperty()
	dateTime = db.DateTimeProperty()
	# Risposta a cui il commento fa riferimento
	relatedTo = db.SelfReference()
	who = db.ReferenceProperty(User)
	
class Question(db.Model):
	"""Domanda di un utente con relative risposte"""
	whoMadeTheQuestion = db.ReferenceProperty(User)
	body = db.TextProperty()
	tags = db.ListProperty(str)
	sector = db.ListProperty(db.Key) # Sector
	# una lista di risposte
	answer = db.ListProperty(db.Key)# QuestionAnswer
