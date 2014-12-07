# -*- coding: latin-1 -*-
import logging, inspect
logging.basicConfig(level = logging.DEBUG)
import pprint, sys, traceback

# estendere con il loggin del chiamante
class L(object):

	@staticmethod
	def getCaller( ):
		"""
		Returns information about the caller
		"""
		return (1,2,3)
		currFrame = inspect.currentframe()
		calframe = inspect.getouterframes( currFrame,0 )
		return (calframe[0][1], calframe[0][3], calframe[0][2])
	@staticmethod
	def _logger( level, message):
		"""
		print the string or dump the object 
		"""
		if type( message ) != type( str() ):
			message = pprint.pformat(message)
		message = "[%s,%s,%s]" % L.getCaller()  + message  
		getattr( logging, level )( message )
		
	@staticmethod
	def info(message ):
		return L._logger( 'info',  message )

	@staticmethod
	def debug(message):
		return  L._logger('info', message)

	@staticmethod
	def warning(message ):
		return L._logger('warning', message)

	@staticmethod
	def critical(message):
		return L._logger('critical', message)
	
	@staticmethod
	def exception( exception ):
		"""
		Logs an exception as critical level
		"""
		exc_type, exc_value, exc_traceback = sys.exc_info()
		tracebackLines = \
			traceback.format_exception( exc_type, exc_value, exc_traceback )

		try:
			fileName, function, line = L.getCaller()
			text = str(exception)
			for line in tracebackLines:
				L.critical("%s,%s,%s,%s"\
						% ( function, fileName,line,text))
			L.critical(''.join( line for line in tracebackLines ))
		except Exception as e:
			L.critical( str(e) )

