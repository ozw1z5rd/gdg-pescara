# -*- coding: latin-1 -*-
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
			'url': 'http://www.yahoo.com',
			'clicks' : 0
		},
		{
			'title' : 'Ulr3', 
			'url': 'http://www.bing.com',
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
			'__user' : 'account1',
			'__email' : 'account1@domain1.com', 
			'lastLogin' : '2012-12-12 00:00:00', 
			'technologies' : list(),
			'allowsMailing' : True,
			'id' : None
		},
		{
			'__user' : 'AccountTwo', 
			'__email' : 'account2@domain.due.com', 
			'lastLogin' : '2013-12-12 11:11:11',
			'technologies' : list(),
			'allowsMailing' : True,
			'id' : None
		}
	)
	
# TODO impostare correttamente i mime type	
	listImages = (
		{
			'description' : 'Prima immagine di test', 
			'link' : 'http://link.alla.prima.immagine/img1.jpg',
			'blob' : None,
			'type' : 'image/jpg',
		},
		{
			'description' : 'Seconda immagine di test', 
			'link' : 'http://seconda.immagine/2.png',
			'blob' : '',
			'type' : 'image/png',
		},
		{
			'description' : 'Terza immagine di test', 
			'link' : 'http://terza.immagine.test/tre.gif',
			'blob' : '',
			'type' : 'image/gif',
		}				
	)
	
	listPost= (
		{
			'title' : 'Titolo 1 del primo post',
			'tags' : list(), 
			'sector' : None, 
			'date' : datetime.datetime.now().strftime('%Y-%m-%d 10:12:11'), 
			'image' : list(),
			'body' : u'Questo è il body del post e conterrà  qualcosa di più del semplice testo', 
			'authors' : list(),
			'repositoryLink' : list(), 
			'reference' : list() 
		},
		{
			'title' : 'Titolo 2 del secondo post',
			'tags' : list(), 
			'sector' : None, 
			'date' : datetime.datetime.now().strftime('%Y-%m-%d 10:12:11'), 
			'image' : list(),
			'body' : u'Questo Ã¨ il testo del secondo post', 
			'authors' : list(),
			'repositoryLink' : list(), 
			'reference' : list() 
		},
		{
			'title' : 'Titolo 3 del terzo post',
			'tags' : list(), 
			'sector' : None, 
			'date' : datetime.datetime.now().strftime('%Y-%m-%d 10:12:11'), 
			'image' : list(),
			'body' : u'Qualcosa di differente rispetto agli altri testi', 
			'authors' : list(),
			'repositoryLink' : list(), 
			'reference' : list() 
		},
		{
			'title' : 'Titolo 4 dell\'ultimo post',
			'tags' : list(), 
			'sector' : None, 
			'date' : datetime.datetime.now().strftime('%Y-%m-%d 10:12:11'), 
			'image' : list(),
			'body' : u'E per adesso 5 post sono piÃ¹ che sufficienti', 
			'authors' : list(),
			'repositoryLink' : list(), 
			'reference' : list() 
		}
			
	)
	
	listRefer = (
		{
			'user' : None,
			'technology' : None, 
			'stars' : 4, 
			'who' : None,
			'description' : 'descrizione uno'
		},
		{
			'user' : None,
			'technology' : None, 
			'stars' : 1, 
			'who' : None,
			'description' : 'altra descrizione'
		},
		{
			'user' : None,
			'technology' : None, 
			'stars' : 2, 
			'who' : None,
			'description' : 'mi sa che...'
		},
		{
			'user' : None,
			'technology' : None, 
			'stars' : 3, 
			'who' : None,
			'description' : 'si sta facendo un po\' tardi'
		},				
	)
	
	listQuestion = (
		{
			'whoMadeTheQuestion' : None, 
			'body' : 'N.1 Di che colore era il notebook bianco di Napoleone?', 
			'tags' : ['TAG1', 'TAG2', 'TAG3', 'bianco', 'TAG5'], 
			'sector' : list(), 
			'answer' : None
		},
		{
			'whoMadeTheQuestion' : None, 
			'body' : 'N.2 Di che colore era il notebook blue di Napoleone?', 
			'tags' : ['TAG1', 'TAG2', 'TAG3', 'blue', 'TAG5'], 
			'sector' : list(), 
			'answer' : None
		},
		{
			'whoMadeTheQuestion' : None, 
			'body' : 'N.3 Di che colore era il notebook rosso di Napoleone?', 
			'tags' : ['TAG1', 'TAG2', 'TAG3', 'rosso', 'TAG5'], 
			'sector' : list(), 
			'answer' : None
		}
	)
	
	listQuestionAnswer = (
		{
			'body' : 'risposta uno delle question answer', 
			'rating' : 1, 
			'dateTime' : '2014-12-12 12:12:13', 
			'relatedTo' : None, 
			'who' : None
		},
		{
			'body' : u'risposta due delle question answer, testo un pò esteso', 
			'rating' : 2, 
			'dateTime' : '2013-10-10 13:13:13', 
			'relatedTo' : None,
			'who' : None
		},
		{
			'body' : u'Altra risposta a questioni oppure ad altre domande', 
			'rating' : 3, 
			'dateTime' : '2012-09-09 12:12:12', 
			'relatedTo' : None, 
			'who' : None
		},
		{
			'body' : u'Ennesima risposta che deve essere linkata da qualche parte', 
			'rating' : 4, 
			'dateTime' : '2011-08-08 11:11:11', 
			'relatedTo' : None, 
			'who' : None
		},
		{
			'body' : u'Ancora un\'altra questione che deve essere linkata', 
			'rating' : 5, 
			'dateTime' : '2010-07-07 10:10:10', 
			'relatedTo' : None, 
			'who' : None
		},
						
	)
