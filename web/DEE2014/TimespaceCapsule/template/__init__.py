#     This file is part of Timespace Capsule.
#
#     Timespace Capsule is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     Timespace Capsule is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with Timespace Capsule.  If not, see <http://www.gnu.org/licenses/>.
#
#     Alessio Palma / 2014
#     fb.com/alessio.palma
#     https://sites.google.com/site/ozw1z5rd/

#
# Very basic template system
#
import logging
logging.basicConfig()

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
            <!DOCTYPE HTML>
            <html>
            <head>
                <title>TemplateBase head</title>
            </head>
        """

    def openBody(self):
        """
        opens the page body
        """
        return "<body>"

    def closeBody(self):
        """
        closes the page body and page too...
        """
        return "</body></html>"

    def _computePage(self):
        """
        does the really hard rendering.
        """
        data = self.html()
        for key in self._dictionary.keys():
            value = self._dictionary[key]
            logging.info("key:{0} value:{1}".format(key, value))
            data = data.replace( "{{"+key+"}}", str(value))
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

