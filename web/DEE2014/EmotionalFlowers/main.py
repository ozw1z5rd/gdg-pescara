#!/usr/bin/env python
# -*- coding: latin-1 -*-
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2

class PaginaUnica(webapp2.RequestHandler):
    def get(self):
        self.response.write("""

			<!DOCTYPE html>
			<html lang="en">
			<head>
				<meta charset="utf-8">
				<meta http-equiv="X-UA-Compatible" content="IE=edge">
				<meta name="viewport" content="width=device-width, initial-scale=1.0">
				<meta name="description" content="">

                <title>TemplateBase head</title>

				<!-- Bootstrap core CSS -->
				<link href="css/bootstrap.css" rel="stylesheet">

				<!-- Custom styles for this template -->
				<link href="css/style.css" rel="stylesheet">

				<!-- Google web Font -->
				<link href='http://fonts.googleapis.com/css?family=Lato:300,400,700,900,100'  rel='stylesheet' type='text/css'>

				<!-- Just for debugging purposes. Don't actually copy this line! -->
				<!--[if lt IE 9]><script src="../../docs-assets/js/ie8-responsive-file-warning.js"></script><![endif]-->

				<!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
				<!--[if lt IE 9]>
					  <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
					  <script src="https://oss.maxcdn.com/libs/respond.js/1.3.0/respond.min.js"></script>
				<![endif]-->
            </head>
			<body>        
				<header>
					<p><a href="http://www.gdg-pescara.org" title="Google Developer Group Pescara Official Site"><img src="img/gdg-pescara.png" class="img-responsive"></a></p>
					<h1><strong>DEE 2014</strong> // Timescape Capsule</h1>
				</header>
				<div class="container">
				
				</div>
			</body>
			</html>
        """);

app = webapp2.WSGIApplication([
    ('/', PaginaUnica)
], debug=False )

