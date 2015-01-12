# -*- coding: latin-1 -*-
#
# 29/12/2014 -> prima bozza
# 09/01/2014 -> qualcosa di più corretto e stabile
#
from google.appengine.ext import db

class Technology(db.Model):
	"""Descrive una delle possibiliti tecnologie trattate"""
	description = db.TextProperty()
	icon = db.BlobProperty()

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
	user = db.UserProperty()
	lastLogin = db.DateTimeProperty()
	technologies = db.ListProperty(UserTechnology)
	def email(self):
		return self.user.email()
	def username(self):	
		return self.user.nickname()
	
class Image(db.Model):
	"""Serve per poter memorizzare le immagini nel datastore"""
	description = db.StringProperty()
	link = db.LinkProperty()
	blob = db.BlobProperty()

class Sector(db.Model):
	"""Settore di interesse, per esempio web development oppure IoT etc...
	ogni articolo viene associato ad un settore"""
	title = db.StringListProperty()
	description = db.StringListProperty()

class Post(db.Model):
	"""descrive un articolo, essenzialmente un articolo puo' far parte di due
	macro categorie: context( news ) e technical ( info tecniche )"""
	title = db.StringProperty()
	tags = db.ListProperty(str)
	sector = db.ListProperty(Sector)
	date = db.DateProperty()
	image = db.ListProperty(Image)
	body = db.TextProperty()
	authors = db.ListProperty(User)
	repositoryLink = db.ListProperty(db.LinkProperty)
	reference = db.ListProperty(db.LinkProperty)
	
# periodicamnete possibile visualizzare quiz per tenere i programmatori 
# "in forma"
class QuizsAnswer(db.Model):
	"""Una delle possibili risposte del quiz"""
	text = db.StringProperty()
	isCorrect = db.BooleanProperty()
	click = db.IntegerProperty()
	# quanto ha risposto
	dateTime = db.DateTimeProperty(auto_now_add=True)

class Quiz(db.Model):
	"""Definisce un quiz come una domanda, un intervallo di validita' per il quiz
	stesso ed una lista di risposte ( di cui una o piu' corretta )"""
	title = db.StringListProperty()
	body = db.TextProperty()
	dateStart = db.DateProperty()
	dateEnd = db.DateProperty()
	answer = db.ListProperty(QuizsAnswer)
	# utenti che hanno gia'  risposto al quiz
	users = db.ListProperty(User)

class Refer(db.Model):
	"""Permette agli utenti di dare referenze ad altri utenti su determinate 
	tecnologie"""
	user = db.ReferenceProperty(User)
	technology = db.ReferenceProperty(Technology)
	stars = db.RatingProperty()
	who = db.ReferenceProperty(User)
	description = db.StringProperty()
	
class QuestionsAnswer(db.Model):
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
	sector = db.ListProperty(Sector)
	# una lista di risposte
	answer = db.ListProperty(QuestionsAnswer)
