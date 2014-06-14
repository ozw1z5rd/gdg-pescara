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


from template.System import SystemLoginTemplate
from google.appengine.api import users
import logging
logging.basicConfig()

def login_required(function):
    def loginRequired(self):
        if users.get_current_user() is not None:
            function(self)
        else:
            loginUrl = users.create_login_url(dest_url=self.request.url)
            page = SystemLoginTemplate({ 'login' : loginUrl })
            return self.response.write( page.render() )
    return loginRequired
