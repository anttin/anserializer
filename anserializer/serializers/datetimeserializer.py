import datetime
from .baseserializer import BaseSerializer


class DatetimeSerializer(BaseSerializer):

  def __init__(self):
    super().__init__([datetime.datetime], '^!Datetime\(\)$')


  def serialize(self, obj):
    return { 
      '!Datetime()': {
         'value':     obj.strftime('%Y-%m-%dT%H:%M:%S.%f'),
         'utcoffset': obj.tzinfo.utcoffset(None).seconds if obj.tzinfo is not None else None,
         'tzname':    obj.tzinfo.tzname(None) if obj.tzinfo is not None else None
       }
    }
     
 
  def deserialize(self, serialized_obj):
    try:
      k, v = list(serialized_obj.items())[0]
    except:
      return serialized_obj

    if 'value' not in v or 'utcoffset' not in v or 'tzname' not in v:
      return serialized_obj

    dt = datetime.datetime.strptime(v['value'], '%Y-%m-%dT%H:%M:%S.%f')
    if v['utcoffset'] is not None and v['tzname'] is not None:
      tz = datetime.timezone(offset=datetime.timedelta(seconds=int(v['utcoffset'])), name=v['tzname'])
      return dt.replace(tzinfo=tz)
    else:
      return dt 
    
