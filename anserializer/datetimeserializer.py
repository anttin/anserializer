import datetime
from objectserializer import ObjectSerializer


class DatetimeSerializer(ObjectSerializer):

  def __init__(self):
    super().__init__([datetime.datetime], '^!Datetime\(\)$')

  def serialize(self, obj):
    tz = obj.astimezone()

    return { 
      '!Datetime()': {
         'value':     obj.strftime('%Y-%m-%dT%H:%M:%S.%f'),
         'utcoffset': tz.utcoffset().seconds,
         'tzname':    tz.tzname()
       }
    }
     
 
  def deserialize(self, obj):
    try:
      k, v = list(obj.items())[0]
    except:
      return obj

    if 'value' not in v or 'utcoffset' not in v or 'tzname' not in v:
      print('ffff')
      return obj

    tz = datetime.timezone(offset=datetime.timedelta(seconds=int(v['utcoffset'])), name=v['tzname'])

    return datetime.datetime.strptime(v['value'], '%Y-%m-%dT%H:%M:%S.%f').replace(tzinfo=tz)
    
