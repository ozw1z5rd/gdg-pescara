from template import TemplateBase

class LoginPageTemplate( TemplateBase ):
    def html(self):
        return """
             <a href="{{login}}">login</a><br>
        """