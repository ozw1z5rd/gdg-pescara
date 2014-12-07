# -*- coding: latin-1 -*-
from protorpc import messages
from protorpc import message_types

package = "TimespaceCapsule"
#
# REQUEST
#

class TSCRequestSearchMessage(messages.Message):
    """Search TSCs
    any search field is optional
    """
    TSCid = messages.IntegerField(1)
    notified = messages.BooleanField(2,default=False)
    assigned = messages.BooleanField(3,default=False)
    anonymous = messages.BooleanField(4,default=False)
    encrypt = messages.BooleanField(5,default=False)
    seen = messages.BooleanField(6,default=False)

class TSCRequesAddtMessage(messages.Message):
    """ Message required to ADD a new TSC
    Some fields are Optional
    Some are mandatory
    """
    lat = messages.FloatField(1)
    lng = messages.FloatField(2)
    tll = messages.IntegerField(3)
    encrypted = messages.BooleanField(4, default=False)
    anonymous = messages.BooleanField(5, default=True)
    content = messages.StringField(6,required=True)
    password = messages.StringField(7)
    openingDate = message_types.DateTimeField(8,required=True)
    closingDate = message_types.DateTimeField(9,required=True)

class TSCRequestOpenMessage( messages.Message):
    """Request capsule to open
    response is the content if any constraint is fine
    otherwise the error code will tell more about the
    problem
    """
    TSCid = messages.IntegerField(1,required=True)
    lat = messages.FloatField(2)
    lng = messages.FloatField(3)
    password = messages.StringField(4)

class TSCRequestRadarMessage(messages.Message):
    """Request target distance
    """
    TSCid = messages.IntegerField(1,required=True)
    lat = messages.FloatField(2,required=True)
    lng = messages.FloatField(3,required=True)


#
# RESPONSE
#
class TSCSingleEntryResponseMessage(messages.Message):
    """ Just a single TSC entry
    """
    TSCid = messages.IntegerField(1)
    lat = messages.FloatField(2)
    lng = messages.FloatField(3)
    tll = messages.IntegerField(4)
    encrypted = messages.BooleanField(5)
    anonymous = messages.BooleanField(6)
    openingDate = message_types.DateTimeField(7)
    closingDate = message_types.DateTimeField(8)
    notifyDate = message_types.DateTimeField(9)
    notified = messages.BooleanField(10)
    user = messages.StringField(11)

class TSCResponseMessage(messages.Message):
    """Standard response
    Header + payload ( one or more TSC entry )
    """
    TSCid = messages.IntegerField(1)
    status = messages.IntegerField(2)
    statusMessage = messages.StringField(3, default='')
    content = messages.StringField(4, default='')
    items = messages.MessageField(
        TSCSingleEntryResponseMessage, 5, repeated=True)

