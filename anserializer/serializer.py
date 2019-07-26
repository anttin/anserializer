import copy
import json
import re
from anserializer.serializers.datetimeserializer import DatetimeSerializer
from anserializer.serializers.objectserializer import ObjectSerializer


class Serializer(object):
  def __init__(self, serializers=[]):
    if len(serializers) == 0:
      self.serializers = [ 
        DatetimeSerializer(),
        ObjectSerializer(object) 
      ]
    else:
      self.serializers = serializers


  def get_serialized(self, obj, **json_dumps_params):
    return self.serialize(obj, self.serializers, **json_dumps_params)


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
  def serialize(cls, obj, serializers, **json_dumps_params):
    _serializers = cls._get_serializer_dict(serializers)
    _obj = cls._prepare_obj_for_serialization(obj, _serializers)

    default_json_dumps_params = { 
      'indent':     2,
      'sort_keys':  True,
      'separators': (',', ': ') 
    }

    _json_dumps_params = { **default_json_dumps_params, **json_dumps_params }

    return json.dumps(_obj, **_json_dumps_params)


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
  def _get_paths(cls, tree, cur=()):
    if not tree:
      yield cur
    else:
      if isinstance(tree, (list, tuple, set)):
        for n in range(len(tree)):
          for path in cls._get_paths(tree[n], cur+(n,)):
            yield path            
      elif isinstance(tree, dict):
        for n, s in tree.items():
          for path in cls._get_paths(s, cur+(n,)):
            yield path
      else:
        yield cur


  @staticmethod
  def _get_path(tree, *keys_or_indexes):
    value = tree
    for key_or_index in keys_or_indexes:
        value = value[key_or_index]
    return value


  @staticmethod
  def _sort_paths_by_length(paths):
    _paths = sorted(paths, key=lambda x: len(x), reverse=True)
    return _paths


  @classmethod
  def _get_longest_paths(cls, paths):
    if paths is None or len(paths) < 1:
      return []

    _paths  = cls._sort_paths_by_length(paths)
    _maxlen = len(_paths[0])

    a = [] 
    for x in _paths:
      if len(x) == _maxlen:
        a.append(x)
      else:
        break
    return a


  @staticmethod
  def _path_get(d, keys):
    for key in keys:
        d = d[key]
    return d


  @classmethod
  def _path_set(cls, d, keys, value):
    d = cls._path_get(d, keys[:-1])
    d[keys[-1]] = value


  @classmethod
  def _finalize_deserialization(cls, obj, deserializers={}, regex_list=[]):
    def check_deserializers(value, regex_list):
      if isinstance(value, dict):
        for k, v in value.items():
          if isinstance(k, str) and len(value.keys()) == 1:
            for r in regex_list:
              if r.search(k):
                return r.pattern
      return None


    paths = [list(x) for x in list(cls._get_paths(obj)) if len(x) > 0]

    _paths = copy.deepcopy(paths)

    processed_paths = set()
    while len(_paths) > 0:
      _longest = cls._get_longest_paths(_paths)

      for path in _longest:
        if not tuple(path) in processed_paths:
          value = cls._path_get(obj, path)
          re_pattern = check_deserializers(value, regex_list)
          if re_pattern is not None:
            cls._path_set(obj, path, deserializers[re_pattern].deserialize(value))
          processed_paths.add(tuple(path))
        path.pop()
        if len(path) == 0:
          _paths.remove(path)

    re_pattern = check_deserializers(obj, regex_list)
    if re_pattern is not None:
      obj = deserializers[re_pattern].deserialize(obj)

    return obj 
        

  @classmethod
  def deserialize(cls, obj_json, serializers):
    deserializers = cls._get_deserializer_dict(serializers)
    _o = json.loads(obj_json)

    regex_list = []
    for r in deserializers.keys():
      regex_list.append(re.compile(r))

    o = cls._finalize_deserialization(_o, deserializers, regex_list)

    return o
    


