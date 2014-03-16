import endpoints
import httplib


# What Where Why error codes.
# See "where" id in classes

class WhereCode( object ):
    WEBSITE_CLASS_GET_METHOD     = '001';
    REST_CLASS                   = '002';

class WhatCode( object ):
    TEMPLATE_EMPTY               = '001';

class WhyCode( object ):
    UNKNOWN                      = '001';


class  A1Exception( endpoints.ServiceException ):
    def __init__(self, what, where, why):
       self.code = "A%sE%sY%s" % ( what, where, why )
    def __str__(self):
        return self.code
    http_status = httplib.INTERNAL_SERVER_ERROR

