from template import TemplateBase

class HomePageTemplate( TemplateBase ):
    def html(self):
        return """
            Benvenuto {{user}}  <a href="{{logout}}">logout</a>
        """