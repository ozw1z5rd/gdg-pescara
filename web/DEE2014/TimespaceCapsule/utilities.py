# -*- coding: latin-1 -*-
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

#
# Utilities, things which does not fit elsewhere
#
from datetime import datetime
from config import TIMEFORMAT, CONVERSION_MAP, MAIL_SENDER
from google.appengine.api import mail


def sendEmail( to, subject, body ):
    """Sends email to "to" using body "body
    """
    return mail.send_mail( sender=MAIL_SENDER, to=to, subject=subject, body=body )
    

def convert(request, key):
    """
    IN -> request, parametername 
    OUT : request paraman converted to pythonish type
          if parametername is not into request/conversion failed 
          -> return None
          
    P.S: date -> datetime 
    """
    t = CONVERSION_MAP[key]
    value = request.get(key)
    # TODO non controlla se ci sono chiavi con valore multipli
    if value is None or len(value) == 0:
        return None
    if t == 'str':
        return str(value)
    elif t == 'boolean':
        if str(value)=="on": # checkbox
            return True
        if int(value) > 0: # numbers
            return True
        return False
    elif t == 'float':
        return float(value)
    elif t == 'date':
        if value is not None:
            return datetime.strptime(value, TIMEFORMAT)
        else: return None
    return value


def validateParams( request, paramList ):
    """
    verifica che la lista dei parametri sia disponibile nella richiesta che 
    è pervenuta al sistema
    
    in : una lista di parametri ed un request
    out : true : ci sono tutti, 
          flase, ne manca almeno uno
    """
    for param in paramList:
        value = request.get(param)
        if value is None or len(str(value)) == 0:
            return False
    return True
    
    

def date2String( date ):
    if date is None:
        return "n.a."
    return date.strftime(TIMEFORMAT)


def parseRequest(request):
    command = "TODO"
    args = dict();
    for param in request.arguments():
        if CONVERSION_MAP.has_key(param):
            args['param'] = convert(request, param, CONVERSION_MAP[param])
    return command, args






