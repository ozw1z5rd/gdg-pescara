from logger import L
import webapp2
from models import Technology, Sector, QuizsAnswer, Quiz, UserTechnology, Link
from test.data import TestData
import datetime

class TestDataLoader(webapp2.RequestHandler):
	"""Load Test data, be sure to load data in the shown order. 
	each method will return true: ALL data loaded, False: at least
	one data entry has gone bad"""
	
	quizAnswerKeys = list()
	technologyEntity = list()
	links = list()
	
	def parseDateTime(self, sDateTime):
		return datetime.datetime.strptime(sDateTime, "%Y-%m-%d %H:%M:%S")
	
	def parseDate(self, sDateTime):
		return self.parseDateTime(sDateTime).date()
	
	def t000(self):
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
		
	def t010(self):
		L.i("SectorTestData load start")
		for el in TestData.listSectors:
			Sector( title = el['title'], description= el['description']).put()
		L.i("SectorTestData load ended")
		return True
	
	def t020(self):
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
	
	def t050(self):
		return True
	def t060(self):
		return True
	def t070(self):
		return True
	def t080(self):
		return True
	def t090(self):
		return True
	
	def get(self):
		L.i("Starting the TestData load")
		if self.t000() and self.t005():
			if self.t010():
				if self.t020():
					if self.t030():
						if self.t040():
							if self.t050():
								if self.t060():
									if self.t070():
										if self.t080():
											if self.t090():
												L.i("Process completed")
												return self.response.write("Data Loaded")
		L.i("Process gone bad")
		return self.response.write("load error")
