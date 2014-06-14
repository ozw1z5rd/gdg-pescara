#     This file is part of Talking Photos.
#
#     Talking Photos is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     Talking Photos is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with Talking Photos.  If not, see <http://www.gnu.org/licenses/>.
#
#     Alessio Palma / 2014
#     fb.com/alessio.palma
#     https://sites.google.com/site/ozw1z5rd/

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
