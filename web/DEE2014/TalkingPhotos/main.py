#!/usr/bin/env python
# -*- coding: latin-1 -*-
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from google.appengine.api import users
from template.loginPageTemplate import LoginPageTemplate
from template.homePageTemplate import HomePageTemplate
import logging
logging.basicConfig()

class TalkingPhotos (webapp2.RequestHandler):


    def loginPage(self):
        login_url = users.create_login_url(self.request.path)
        page = LoginPageTemplate({ 'login' : login_url })
        self.response.write( page.render() )

    def homePage(self):
        logout_url = users.create_logout_url(self.request.path)
        nick = users.get_current_user().nickname()
        page = HomePageTemplate({ 'logout' : logout_url, 'user': nick })
        self.response.write( page.render() )

    def visitorPage(self):
        pass

    def allowed(self, who):
        return True

    def get(self):
        user = users.get_current_user( )
        if user is None:
            return self.loginPage()
        if self.allowed( user ) :
            return self.homePage()
        return self.visitorPage()

app = webapp2.WSGIApplication([
    ('/', TalkingPhotos)
], debug=False )

