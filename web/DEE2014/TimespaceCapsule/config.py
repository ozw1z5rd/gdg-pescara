# -*- coding: latin-1 -*-
#
#  Configuration
#

TIMEFORMAT = "%d/%m/%Y" # 31/01/2010

# conversion table ( GET/POST parameter -> python type )
CONVERSION_MAP = {
    'txtOpenDate' : 'date',
    'txtCloseDate' : 'date',
    'txtContent' : 'str',
    'txtLatitude' : 'float',
    'txtLongitude' : 'float',
    'chkAnonymous' : 'boolean',
    'chkEncrypted' : 'boolean'
}

# where this service is running
SERVERNAME="http://timespacecapsule.appspot.com"

APPID="this-app-id"

# who is sending the email to user.
MAIL_SENDER="ozw1z5rd@gmail.com"

# meters
POSITION_DEFAULT_TLL = 150
