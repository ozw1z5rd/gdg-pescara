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
    elif t == 'float':
        return float(value)
    elif t == 'date':
        return datetime.strptime(value, TIMEFORMAT )
    return None

    return request.get(key)