import json
import re
from datetimeserializer import DatetimeSerializer
from objectserializer import ObjectSerializer


"""

Serializer can be utilized either as instantiated or non-instantiated.


Instantiated example:
------------------------

s = serializer.Serializer([ serializer.DatetimeSerializer(), serializer.ObjectSerializer(object), serializer.MySerializer(MyClass) ])
x = ser.get_serialized(o)
_x = ser.get_deserialized(x)


Non-instantiated example:
-------------------------

serializers = [ serializer.DatetimeSerializer(), serializer.ObjectSerializer(object), serializer.MySerializer(MyClass) ]
x = serializer.Serializer.serialize(o, serializers)
_x = serializer.Serializer.deserialize(x, serializers)


"""

class Serializer(object):
  def __init__(self, serializers=[]):
    if len(serializers) == 0:
      self.serializers = [ 
        DatetimeSerializer(),
        ObjectSerializer(object) 
      ]
    else:
      self.serializers = serializers


  def get_serialized(self, o):
    return self.serialize(o, self.serializers)


  def get_deserialized(self, j):
    return self.deserialize(j, self.serializers)


  @classmethod
  def _prepare_obj_for_serialization(cls, o, serializers={}):

    if isinstance(o, (int, float, complex, str, bool)):
      return o

    elif isinstance(o, (tuple, list, set)):
      _o = []
      for item in o:
        _o.append(cls._prepare_obj_for_serialization(item, serializers))

      if isinstance(o, tuple):
        return tuple(_o)
      elif isinstance(o, set):
        return set(_o)
      else:
        return _o

    elif isinstance(o, dict):
      _o = {}
      for k, v in o.items():
        _o[k] = cls._prepare_obj_for_serialization(v, serializers)
      return _o

    else:
    
      if type(o) in serializers.keys():
        _o = serializers[type(o)].serialize(o)
        if isinstance(_o, (tuple, list, set)):
          a = []
          for v in _o:
            a.append(cls._prepare_obj_for_serialization(v, serializers))
          return a
        elif isinstance(_o, dict):
          d = {}
          for k, v in _o.items():
            d[k] = cls._prepare_obj_for_serialization(v, serializers)
          return d
 
      return o


  @classmethod
  def serialize(cls, obj, serializers=[]):
    _serializers = cls._get_serializer_dict(serializers)
    _obj = cls._prepare_obj_for_serialization(obj, _serializers)
    return json.dumps(_obj, indent=4, sort_keys=True, separators=(',', ': '))


  @staticmethod
  def _get_serializer_dict(serializer_list):
    if not isinstance(serializer_list, list):
      raise Exception('Serializer list is not a list!') 

    result = {}
    for serializer in serializer_list:
      result = { **result, **serializer.get_obj_type_dict() }

    return result


  @staticmethod
  def _get_deserializer_dict(serializer_list):
    if not isinstance(serializer_list, list):
      raise Exception('Serializer list is not a list!') 

    result = {}
    for serializer in serializer_list:
      result = { **result, **serializer.get_id_regex_dict() }

    return result


  @classmethod
  def _finalize_deserialization(cls, obj, deserializers={}, regex_list=[]):
    if isinstance(obj, list):
      a = []
      for item in obj:
        a.append(cls._finalize_deserialization(item, deserializers, regex_list))
      return a
        
    elif isinstance(obj, dict):
      o = {}
      for k, v in obj.items():
        if isinstance(k, str) and len(obj.keys()) == 1:
          for r in regex_list:
            if r.search(k):
              return deserializers[r.pattern].deserialize(obj)
        o[k] = cls._finalize_deserialization(v, deserializers, regex_list)
        
      return o      

    else:
      return obj
     
    
  @classmethod
  def deserialize(cls, obj_json, serializers=[]):
    deserializers = cls._get_deserializer_dict(serializers)
    _o = json.loads(obj_json)

    regex_list = []
    for r in deserializers.keys():
      regex_list.append(re.compile(r))

    o = cls._finalize_deserialization(_o, deserializers, regex_list)

    return o
    


