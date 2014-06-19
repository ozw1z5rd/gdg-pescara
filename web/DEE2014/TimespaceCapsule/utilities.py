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
TIMEFORMAT = "%d/%m/%Y" # 31/01/2010

def convert(request, key, t):
    value = request.get(key)
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
            return datetime.strptime(value, TIMEFORMAT )
        else: return None

    return value


def date2String( date ):
    if date is None:
        return "n.a."
    return date.strftime("%d-%m-%Y")