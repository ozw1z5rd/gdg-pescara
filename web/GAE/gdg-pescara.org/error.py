import endpoints
import httplib


# What Where Why error codes.
# See "where" id in classes

class WhereCode( object ):
    WEBSITE_CLASS_GET_METHOD     = '001'
    REST_CLASS                   = '002'
    REST_CLASS_GETMODEL_METHOD   = '003'

class WhatCode( object ):
    TEMPLATE_EMPTY               = '001'
    AUTH                         = '002'
    PARAMETER_ERROR              = '003'
    PARSE_ERROR                  = '004'

class WhyCode( object ):
    UNKNOWN                      = '001'
    NO_USER_PROVIDED             = '002'
    NO_VALID_USER_PROVIDED       = '003'
    MODEL_NOT_AVAILABLE          = '004'
    PARAMETER_VALUE_ERROR        = '005'
    MALFORMED_JSON               = '006'
    NOT_EXISTING_FIELD_IN_MODEL  = '007'
    MISSING_ENTITY_ID            = '008'

class DefaultException( endpoints.ServiceException ):
    def __init__(self, what, where, why):
       self.code = "A%sE%sY%s" % ( what, where, why )
    def __str__(self):
        return self.code

class S1Exception( DefaultException ):
    http_status = httplib.UNAUTHORIZED

class A1Exception( DefaultException ):
    http_status = httplib.INTERNAL_SERVER_ERROR
  
 
