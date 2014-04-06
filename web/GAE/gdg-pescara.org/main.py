#!/usr/bin/env python
# -*- coding: latin-1 -*-
#
#  Main.py
#
#    In : http request
#   Out : return the answer from the loaed module
#
import webapp2
from website import Website
from rest import Api 
from runOnce import Init 

app = webapp2.WSGIApplication(
         [ 
   	      webapp2.Route(r'/rest/<entity>/<eid>', Api, name='single' ),  
   	      webapp2.Route(r'/rest/<entity>', Api, name='list' ),  
              webapp2.Route(r'/', Website, name='home'),
              webapp2.Route(r'/initialize', Init, name='init' )
         ], 
         debug=False
      )
