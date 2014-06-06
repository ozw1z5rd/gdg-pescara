from template import TemplateBase

# if user goes is here is logged ( authenticated by the app )
class VisitorPageTemplate( TemplateBase ):
    def html(self):
        return """
            Salve {{user}}, attualmente non sei autorizzato ad accedere alla risorsa
            clicca il link seguente per inviare una email per richiedere l'autorizzazione<br>
            Richiesta autorizzazione  <a href="{{authreq}}">authreq</a>
            <br><a href="{{logout}}>logout</a>
        """

class VisitorWaitTemplate( TemplateBase ):
    def html( self ):
        return """
            Richiesta di autorizzazione inviata. Riceverai una email non
            appena possibile.
            <br><a href="{{logout}}">logout</a>
        """

class VisitorActivatedTemplate(TemplateBase):
    def html(self):
        return """
            Utente {{email}} attivato, ora puo' accedere alla risorsa
        """

class VisitorActivatedErrorTemplate(TemplateBase):
    def html(self):
        return """
            Impossibile attivare: {{email}}, forse email errata oppure
            utente di amministrazione errata.
        """



class VisitorActivatedDebugTemplate(TemplateBase):
    def html(self):
        return """
            Clicca per attivare: <a href="/authorize?email={{email}}">/authorize?email={{email}}</a>
        """
