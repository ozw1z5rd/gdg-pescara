# -*- coding: latin-1 -*-
from logger import L
import webapp2
from models import Technology, Sector, QuizsAnswer, Quiz, \
UserTechnology, Link, User, Refer, Post, Image, QuestionAnswer, Question
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
	refers = list()
	images = list()
	questions = list()
	questionAnswers = list()
	
	def parseDateTime(self, sDateTime):
		return datetime.datetime.strptime(sDateTime, "%Y-%m-%d %H:%M:%S")
	
	def parseDate(self, sDateTime):
		return self.parseDateTime(sDateTime).date()
	
	def getRandomString(self, size):
		return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))
	
	def getRandomText(self, rows, cols):
		return '\n'.join( self.getRandomString(cols) for _ in range(rows) )
	
	def listOf(self, lst, n):
		return [ random.choice(lst) for _ in xrange(n) ] 
	
	def t000_Technology(self):
		"""Lista delle tecnologie"""
		L.i("TecnologyTestData load start")
		c = 0
		for el in TestData.listTechnologies:
			L.i("    Dataloaded #{0}".format(c)); c+=1;
			technology = Technology(
				title = el['title'],
				description=el['description'],
				icon="nunce")
			self.technologyEntity.append(technology)
			technology.put()
		L.i("TechnologyTestData load ended")
		return True
	
	def t005_Link(self):
		"""lista dei link"""
		L.i("LinkTestData load start")
		c = 0 
		for el in TestData.listLinkProperty:
			L.i("    Dataloaded #{0}".format(c)); c+=1;
			link = Link(
					title = el['title'],
					url = el['url'],
					clicks = el['clicks']
				)
			link.save()
			self.links.append(link)
		L.i("LinkTestData load ended")
		return True
		
	def t010_Sector(self):
		"""Settori di applicazione"""
		L.i("SectorTestData load start")
		c = 0 
		for el in TestData.listSectors:
			L.i("    Dataloaded #{0}".format(c)); c+=1;
			sector =  Sector( title = el['title'], description= el['description'])
			self.sectors.append(sector)
			sector.put()
		L.i("SectorTestData load ended")
		return True
	
	def t020_QuizAnswer(self):
		"""Possibili risposte ai quiz"""
		L.i("QuizAnswerTestData load start")
		c= 0
		for el in TestData.listQuizAnswer:
			L.i("    Dataloaded #{0}".format(c)); c+=1;
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
	
	def t030_Quiz(self):
		"""Quiz, le domande a risposta multipla"""
		L.i("QuizTestData load start")
		c = 0
		for el in TestData.listQuiz:
			L.i("    Dataloaded #{0}".format(c)); c+=1;
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
	
	def t040_UserTechnology(self):
		"""tecnologie a cui un utente può essere associato"""
		L.i("UserTechnologyTestData load start")
		if len(self.technologyEntity) == 0:
			return False
		c = i = 0
		for el in TestData.listUserTecnology:
			L.i("    Dataloaded #{0}".format(c)); c+=1;
			UserTechnology(
				technology = self.technologyEntity[i], 
				rating = el['rating']
			).put()
			i += 1
		L.i("UserTechnologyTestData load ended")
		return True
	
	def t045_User(self):
		"""Accounts"""
		L.i("UserTestData load start")
		c = 0
		for el in TestData.listUser:
			L.i("    Dataloaded #{0}".format(c)); c+=1;
			user = User(
				user_id = self.getRandomString(20),
				__email = el['__email'],
				__user = el['__user'], 
				federated_identity = None
			)
			self.users.append(user)
			user.put()
		L.i("UserTestData load ended")
		return True

	def t050_Refer(self):
		"""I like"""
		L.i("ReferTestData load start")
		nu = len(self.users)
		nt = len(self.technologyEntity)
		c = 0
		if ( nu ==0 ):
			L.w("No uses available to load refers")
			return False
		if ( nt == 0):
			L.w("No techs available for refers ")
			return False
		L.i("found {0} user and {1} technology entries".format(nu,nt))
		for el in TestData.listRefer:
			ref = Refer(
				user = random.choice(self.users), 
				technology = random.choice(self.technologyEntity),
				stars = el['stars'],
				who = random.choice(self.users), 
				description = el['description']
			)
			self.refers.append(ref)
			ref.save()
			L.i("    Dataloaded #{0}".format(c)); c+=1;
		L.i("ReferTestData load ended")
		return True
	
	def t060(self):
		return True
	
	def t065_Image(self):
		"""Immagini"""
		L.i("ImageTestData load start")
		for el in TestData.listImages:
			img = Image(
				description = el['description'], 
				link = el['link'], 
				type = el['type'],
				blob = el['blob']
			)
			self.images.append(img)
			img.save()
		L.i("ImageTestData ended")
		return True
	
	def t070_Post(self):
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
		c = 0
		for el in TestData.listPost:
			ref = list( [ x.key() for x in self.listOf( self.links, 4) ])
			L.i("    Dataloaded #{0}".format(c)); c+=1;
			L.i(ref);
			post = Post( 
				title = el['title'], 
				tags = ["tag1", "tags2", "tag3"], 
				sector = list( [x.key() for x in self.listOf( self.sectors,2 )] ),
				date = self.parseDate(el['date']),
				image = list( [ x.key() for x in self.listOf( self.images, 2)]), 
				body = unicode(el['body']),
				author = random.choice(self.users), 
				repositoryLink = list( [x.key() for x in self.links]), 
				reference = ref
 			)
			post.save()
		L.i("PostTestData load ended")
		return True
	
	def t075_QuestionAnswer(self):
		"""QuestionAnswer"""
		L.i("QuestionAnswerTestData load start")
		L.i("  building the questionAnswer list")
		c = 0
		for el in TestData.listQuestionAnswer:
			qa = QuestionAnswer(
				body = el['body'], 
				rating = el['rating'], 
				dateTime = self.parseDateTime(el['dateTime']),
				relatedTo = None,
				who = random.choice(self.users)
			)
			self.questionAnswers.append(qa)
			qa.save()
			L.i("    Dataloaded #{0}".format(c)); c+=1;
		L.i("  questionAnswer list built")
		L.i("  cross linking")
		for i in xrange(len(self.questionAnswers)):
			self.questionAnswers[i].relatedTo = \
				random.choice( self.questionAnswers[0:i] + self.questionAnswers[(i+1):]) 
		L.i("  cross linking ended")	
		L.i("QuestionAnswerTestData load ended")
		return True
	
	def t080_Question(self):
		L.i("QuestionTestData load start")
		c = 0
		for el in TestData.listQuestion:
			q = Question(
				whoMadeTheQuestion = random.choice(self.users),
				body = el['body'],
				tags = el['tags'], 
				sector = list( [ x.key() for x in self.listOf(self.sectors,2)]),
				answer = [ random.choice(self.questionAnswers).key() ]
			)
			q.save()
			L.i("    Dataloaded #{0}".format(c)); c+=1;
		L.i("QuestionTestData load ended")
		return True
	
	def t090(self):
		return True
	
	# Attenzione all'ordine di caricamento dei dati per le dipendenze annesse
	def get(self):
		L.i("Starting the TestData load")
		if self.t000_Technology() : 
			if self.t005_Link():
				if self.t010_Sector():
					if self.t020_QuizAnswer():
						if self.t030_Quiz():
							if self.t040_UserTechnology():
								if self.t045_User():
									if self.t050_Refer():
										if self.t065_Image():
											if self.t070_Post():
												if self.t075_QuestionAnswer():
													if self.t080_Question():
														L.i("Process completed")
														return self.response.write("Data Loaded")
		L.i("Process gone bad")
		return self.response.write("load error")
