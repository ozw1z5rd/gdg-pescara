from template import TemplateBase

class SystemLoginTemplate(TemplateBase):
    def html(self):
        return """
            SYSTEM :: Please login <a href="{{login}}">Click here to login</a>
        """
