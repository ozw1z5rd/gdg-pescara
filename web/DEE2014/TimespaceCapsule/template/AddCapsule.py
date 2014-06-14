#     This file is part of Timespace Capsule.
#
#     Timespace Capsule is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     Timespace Capsule is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with Timespace Capsule.  If not, see <http://www.gnu.org/licenses/>.
#
#     Alessio Palma / 2014
#     fb.com/alessio.palma
#     https://sites.google.com/site/ozw1z5rd/

from template import TemplateBase

class AddCapsuleFormTemplate(TemplateBase):
    def html(self):
        return """
          <form action="/add" method="POST">
          <ul>
              <li>Opening Date:<input type="text" name="txtOpenDate"></input>
              <li>Closing Date:<input type="text" name="txtCloseDate"></input>
              <li>Content:<input type="text" name="txtContent"></input>
              <li>latitude:<input type="text" name="txtLatitude"></input>
              <li>longitude:<input type=text" name="txtLongitude"></input>
              <li>Tollerance:<input type="text" name="txtTollerance"></input>
              <input type="submit">
          </form>
        """

class AddCapsuleOkTemplate(TemplateBase):
    def html(self):
        return """
            <h3>Capsule created</h3>
            <br>Capsule id:<b>{{tscid}}</b>
            <ul>
            <li>opening date:{{openingDate}}
            <li>closing date:{{closingDate}}
            <li>Content: {{content}}
            <li>latitude: {{latitude}}
            <li>longitude: {{longitude}}
            <li>tollerance(m): {{tollerance}}
            </ul>
        """

class AddCapsuleKoTemplate(TemplateBase):
    def html(self):
        return """
            <h3>Capsule Not created</h3>
        """