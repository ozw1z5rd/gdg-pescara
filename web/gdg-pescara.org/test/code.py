# -*- coding: latin-1 -*-
from logger import L
import webapp2
from models import Technology, Sector, QuizsAnswer, Quiz, UserTechnology, Link, User
from test.data import TestData
import datetime, string, random

class TestDataLoader(webapp2.RequestHandler):
	"""Load Test data, be sure to load data in the shown order. 
	each method will return true: ALL data loaded, False: at least
	one data entry has gone bad"""
	
	quizAnswerKeys = list()
	technologyEntity = list()
	links = list()
	users= list()
	sectors = list()
	
	def parseDateTime(self, sDateTime):
		return datetime.datetime.strptime(sDateTime, "%Y-%m-%d %H:%M:%S")
	
	def parseDate(self, sDateTime):
		return self.parseDateTime(sDateTime).date()
	
	def getRandomString(self, size):
		return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))
	
	def getRandomText(self, rows, cols):
		return '\n'.join( self.getRandomString(cols) for _ in range(rows) )
	
	def t000(self):
		"""Lista delle tecnologie"""
		L.i("TecnologyTestData load start")
		for el in TestData.listTechnologies:
			L.i(el)
			technology = Technology(
				title = el['title'],
				description=el['description'],
				icon="nunce")
			self.technologyEntity.append(technology)
			technology.put()
		L.i("TechnologyTestData load ended")
		return True
	
	def t005(self):
		"""lista dei link"""
		L.i("LinkTestData load start")
		for el in TestData.listLinkProperty:
			self.links.append(
				Link(
					title = el['title'],
					url = el['url'],
					clicks = el['clicks']
				)
			)
		L.i("LinkTestData load ended")
		return True
		
	def t010(self):
		"""Settori di applicazione"""
		L.i("SectorTestData load start")
		for el in TestData.listSectors:
			sector =  Sector( title = el['title'], description= el['description'])
			self.sectors.append(sector)
			sector.put()
		L.i("SectorTestData load ended")
		return True
	
	def t020(self):
		"""Possibili risposte ai quiz"""
		L.i("QuizAnswerTestData load start")
		for el in TestData.listQuizAnswer:
			quizAnswer = QuizsAnswer( 
				text = el['text'],
				isCorrect=el['isCorrect'],
				click=el['click']
			)
			quizAnswer.put()
			self.quizAnswerKeys.append(
				quizAnswer.key()
			)
		L.i("QuizAnswerTestData load ended")
		return True
	
	def t030(self):
		"""Quiz, le domande a risposta multipla"""
		L.i("QuizTestData load start")
		for el in TestData.listQuiz:
			Quiz(
				title = el['title'],
				body = el['body'],
				dateStart = self.parseDate(el['dateStart']),
				dateEnd = self.parseDate(el['dateEnd']),
				answer= [ self.quizAnswerKeys[0] ], # todo -> deve recuperare i dati dal passo precedente
				user = el['user']
			)
		L.i("QuizTestData load ended")
		return True
	
	def t040(self):
		"""tecnologie a cui un utente può essere associato"""
		L.i("UserTechnologyTestData load start")
		if len(self.technologyEntity) == 0:
			return False
		i = 0
		for el in TestData.listUserTecnology:
			UserTechnology(
				technology = self.technologyEntity[i], 
				rating = el['rating']
			).put()
			i += 1
		L.i("UserTechnologyTestData load ended")
		return True
	
	def t045(self):
		"""Accounts"""
		L.i("UserTestData load start")
		for el in TestData.listUser:
			user = User(
				user_id = self.getRandomString(20),
				email = el['email'], 
				federated_identity = None
			)
			self.users.append(user)
			user.put()
		L.i("UserTestData load ended")
		return True

	def t050(self):
		"""I like"""
		L.i("ReferTestData load start")
		nu = len(self.users)
		nt = len(self.technologyEntity)
		if ( nu ==0 ):
			L.w("No uses available to load refers")
			return False
		if ( nt == 0):
			L.w("No techs available for refers ")
			return False
		L.i("ReferTestData load ended")
		return True
	
	def t060(self):
		return True
	
	def t070(self):
		"""articoli"""
		L.i("PostTestData load start")
		nu = len( self.users)
		ns = len( self.sectors) 
		if not nu:
			L.w("No user to use to load user post :-) ")
			return False
		if not ns:
			L.w("No sectors available")
			return False
		
		for el in TestData.listPost:
# 			post = Post( 
# 				title = '', 
# 				tags = '', 
# 				sector = '', 
# 				date = self.parseDateTime(sDateTime),
# 				image = None, 
# 				body = self.getRandomText(80, 40),
# 				author = '', 
# 				repositoryLink = '', 
# 				reference = ''
# 			)
			pass
		L.i("PostTestData load ended")
		return True
	
	def t075(self):
		return True
	def t080(self):
		return True
	def t090(self):
		return True
	
	# Attenzione all'ordine di caricamento dei dati per le dipendenze annesse
	def get(self):
		L.i("Starting the TestData load")
		if self.t000() and self.t005():
			if self.t010():
				if self.t020():
					if self.t030():
						if self.t040() and self.t045():
							if self.t050():
								if self.t060():
									if self.t070() and self.t075():
										if self.t080():
											if self.t090():
												L.i("Process completed")
												return self.response.write("Data Loaded")
		L.i("Process gone bad")
		return self.response.write("load error")
