from template import TemplateBase

class OpenCapsuleTemplate(TemplateBase):
    def html(self):
        return """
            Content: <a href="{{content}}">{{content}}</a>
        """