#
# This file will load some test data into the datastore
#


import webapp2
from logger import L
from test.code import TestDataLoader

# 
# def loadTestData(webapp2.RequestHandler):
# 	for el in listTechnologies.keys():
# 		Technology(description=el,icon="Nunce").put()
	
	
class Home(webapp2.RequestHandler):
	"""TO DO"""
	def get(self):
		L.i("called Home")
		return self.response.write("It's Working! click here to load the data : <a href=\"/testData\">LOAD</a>")


app = webapp2.WSGIApplication([
    ('/', Home),
    ('/testData', TestDataLoader ) # from test.code
], debug=	True )
