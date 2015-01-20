from google.appengine.api import users
from endpointMessages import GDGPEEmptyResponse

class temp():
	parameter = ""
	def __init__(self):
		pass
	
	def __call__(self):
		pass
	
def requireValidUser(function):
	"""Torna un redirect oppure continua con il metodo invocato"""
	def _requireValidUser(*args): 
		user = users.get_current_user()
		if user is None:
			redirectUlr = "TODO"
			redirectUlr += "pO"
			return GDGPEEmptyResponse()
		function(*args)
	return _requireValidUser