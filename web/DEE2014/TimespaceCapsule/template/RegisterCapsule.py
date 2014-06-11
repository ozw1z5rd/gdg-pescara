from template import TemplateBase

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
