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
