#     This file is part of Talking Photos.
#
#     Talking Photos is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     Talking Photos is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with Talking Photos.  If not, see <http://www.gnu.org/licenses/>.
#
#     Alessio Palma / 2014
#     fb.com/alessio.palma
#     https://sites.google.com/site/ozw1z5rd/

#
# Very basic template system
#
import logging

class TemplateBase( object ):

    _cacheValid = False
    _cache = ""
    _dictionary = { }

    def html(self):
        """
        returns the html template to render
        this is private method
        """
        return """
            You should define your own template file
            this is from TemplateBase and it is not
            suitable for your purposes.
        """

    def head(self):
        """
        return the page header section and starts the html
        """
        return """
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
        """

    def openBody(self):
        """
        opens the page body
        """
        return """
			<body>        
				<header>
					<p><a href="http://www.gdg-pescara.org" title="Google Developer Group Pescara Official Site"><img src="img/gdg-pescara.png" class="img-responsive"></a></p>
					<h1><strong>DEE 2014</strong> // Talking Photos</h1>
				</header>
				<div class="container">
		"""

    def closeBody(self):
        """
        closes the page body and page too...
        """
        return "</div></body></html>"

    def _computePage(self):
        """
        does the really hard rendering.
        """
        data = self.html()
        for key in self._dictionary.keys():
            value = self._dictionary[key]
            data = data.replace( "{{"+key+"}}", value)
        return data

    def render(self):
        """
        renders the template and store the result into the cache
        """
        logging.info("Entering render")
        if self._cacheValid:
            return self._cache
        self._cache += self.head()
        self._cache += self.openBody()
        self._cache += self._computePage()
        self._cache += self.closeBody()
        return self._cache

    def update(self, dictionary):
        """
        update the values which will be replaced into the template
        """
        self._cacheValid = False
        self._dictionary = dictionary

    def __init__(self , dictionary ):
        self._dictionary = dictionary
