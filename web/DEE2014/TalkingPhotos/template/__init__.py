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
