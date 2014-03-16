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
   	      ( '/rest', Api ),  
              ('/', Website),
              ('/initialize', Init )
         ], 
         debug=True
      )
