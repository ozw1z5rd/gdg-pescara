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

class LoginPageTemplate( TemplateBase ):
    def html(self):
        return """
            <h3 class="bg-info"><a href="{{login}}">login</a><br></h3>
        """