from models import Technology
from config import Configuration
from logger import L

# 
# Il controller prende in input endpointMessage e torna endPointMessages
# 
# [C]reate
# [U]pdate
# [R]etrieve
# [D]elete
# [L]ist retrieve
#

class UserController(object):
	pass

class PostController(object):
	pass


class TechnologyController(object):
	
	def c(self,request):
		pass
	
	def u(self,request):
		pass
	
	def r(self,request):
		pass
	
	def d(self,request):
		pass

	def getList(self,request):
		return  list([ x.asMessageElement() for x in Technology.all() ])


