from template import TemplateBase

class RegisterCapsuleLoginTemplate(TemplateBase):
    def html(self):
        return """
            Please login <a href="{{login}}">Click here to login</a>
        """

class RegisterCapsuleTemplate(TemplateBase):
    def html(self):
        return """
            Capsule registered, check email  <a href="{{logout}}">Click here to logout</a>
        """

class RegisterCapsuleErrorTemplate(TemplateBase):
    def html(self):
        return """
            Sorry: {{message}}
        """
