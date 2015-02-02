import datetime

class TestData(object):
	"""Test data to load"""
	
	listLinkProperty = (
		{
			'title' : 'Url1', 
			'url': 'http://www.google.com',
			'clicks' : 0
		},
		{
			'title' : 'Url2', 
			'url': 'www.yahoo.com',
			'clicks' : 0
		},
		{
			'title' : 'Ulr3', 
			'url': 'www.bing.com',
			'clicks' : 0
		}
	)
	
	listSectors =  (
		{ 'title' : 'Web', 'description' : 'webdevelopment' } , 
		{ 'title' : 'JS', 'description' : 'javascript'},
	)

	listTechnologies = (
		{ 'title' : 'javascript' , 'description': "please replace with dart"},
		{ 'title' : 'java','description' : "evergreen language" },
		{ 'title' : 'dart' , 'description' : "hope this will replace soon js"},
		{ 'title' : 'C++' , 'description' : "can save your life is correctly used"},
		{ 'title' : 'go' , 'description' : 'dunno'},
		{ 'title' : 'polymer', 'description' : 'play with Lego brick'	},
		{ 'title' : 'angularjs', 'description' : "nice framework" }
	)
	
	listQuizAnswer = ( 
		{ 'text' : 'Answer1Quiz1', 'isCorrect': False, 'click' : 0 },
		{ 'text' : 'Answer2Quiz1', 'isCorrect': True, 'click' : 0 },		
	    { 'text' : 'Answer1Quiz2', 'isCorrect': False, 'click' : 0 },
	    { 'text' : 'Answer2Quiz2', 'isCorrect': True, 'click' : 0 },
	    { 'text' : 'Answer1Quiz3', 'isCorrect': False, 'click' : 0 },
	    { 'text' : 'Answer2Quiz3', 'isCorrect': True, 'click' : 0 },
	    { 'text' : 'Answer3Quiz3', 'isCorrect': False, 'click' : 0 }
	)
	
	# il campo answer deve essere parsato ed indica la posizione ordinale 
	# della risposta nella lista delle risposte ai quia
	listQuiz = ( 
		{ 
		  'title' : 'Quiz1', 
		  'body': 'Switch per eseguire il controllo sintattico di uno script', 
		  'dateStart' : '2020-10-10 00:00:00', 
		  'dateEnd' : '2020-11-10 23:59:59', 
		  'answer' :None, 
		  'user' : None 
		},
		{ 
		  'title' : 'Quiz2', 
		  'body': 'Variabile che contiene il separatore di campo in AWK', 
		  'dateStart' : '2010-10-10 00:00:00', 
		  'dateEnd' : '2020-10-10 23:59:59', 
		  'answer' : [2,3], 
		  'user' : None 
		},
		{ 
		  'title' : 'Quiz3', 
		  'body': 'verificare tutte le immagini disponibili in docker', 
		  'dateStart' : '2009-10-10 00:00:00', 
		  'dateEnd' : '2030-10-10 00:00:00', 
		  'answer' : [4,5,6 ], 
		  'user' : None
		}			
	)
	
	# all User Technology will reference the 1st technology entity
	listUserTecnology = (
		{
			'technology' : None, 
			'rating': 0 
		},
		{
			'technology' : None,
			'rating' : 1 
		}
	)
	
	listUser = (
		{
			'user' : '', 
			'lastLogin' : '2012-12-12 00:00:00', 
			'technologies' : list(),
			'allowsMailing' : True, 
		}
	)
	
	listPost= (
		{
			'title' : '',
			'tags' : list(), 
			'sector' : None, 
			'date' : datetime.datetime.now().strftime('%Y-%m-%d 10:12:11'), 
			'image' : list(),
			'body' : '', 
			'authors' : list(),
			'repositoryLink' : list(), 
			'reference' : list() 
		}
	)
	
	listRefer = ()
	
	listQuestion = (
		{
			'whoMadeTheQuestion' : None, 
			'body' : '', 
			'tags' : list(), 
			'sector' : list(), 
			'answer' : None
		}
	)
	
	listQuestionAnswer = ()
	
	