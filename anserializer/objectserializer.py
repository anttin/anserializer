import re

class ObjectSerializer(object):
  def __init__(self, obj_types, id_regex = '^!Class\((([a-zA-Z_][0-9a-zA-Z_]*)\.([a-zA-Z_][0-9a-zA-Z_]*))?\)$'):
    if isinstance(obj_types, list):
      self._obj_types = obj_types
    else:
      self._obj_types = [ obj_types ]

    self.id_regex = id_regex


  def get_obj_type_dict(self):
    types = {}
    for _type  in self._obj_types:
      types[_type] = self
    return types


  def get_id_regex_dict(self):
    return { self.id_regex: self }


  # override this for custom operation
  def serialize(self, obj, class_identifiers_in_params=False):
    if class_identifiers_in_params:
      result = { 
        '!Class()': {
          '__module__': obj.__module__, 
          '__class__':  obj.__class__.__name__,
          **obj.__dict__
        }
      }
    else:  
      result = { '!Class({}.{})'.format(obj.__module__, obj.__class__.__name__, ):  { **obj.__dict__ } }

    return result


  # override this for custom operation
  def deserialize(self, obj):
    # structure should be like this: { '!Object(Module.Class)': { ... params ... } } so only one item in the dict
    try:
      k, v = list(obj.items())[0]
    except:
      return obj
    
    r = re.match(ID_REGEX, k)

    if not r:
      return obj

    if r.groups()[0] is None and '__class__' in v and '__module__' in v:
      module_name = v.pop("__module__")
      class_name  = v.pop("__class__")
    elif r.groups()[0] is not None and r.groups()[1] is not None and r.groups()[2] is not None:
      module_name = r.groups()[1] 
      class_name  = r.groups()[2]
      
    module = __import__(module_name)
    cls    = getattr(module, class_name)
    _obj   = cls(**v)

    return _obj

