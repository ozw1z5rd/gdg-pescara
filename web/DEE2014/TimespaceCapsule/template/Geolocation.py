from template import TemplateBase

class GeolocationTemplate(TemplateBase):

    def head(self):
        """
        Just add javascript to allow geolocation
        """
        return """
            <!DOCTYPE HTML>
            <html>
            <head>
                <title>TemplateBase head</title>
            </head>
        """

    def html(self):
        return """
        """