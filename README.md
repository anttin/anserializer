# anserializer

A module for serializing and deserializing complex data structures to/from json. It allows the user to (de)serialize a complex dictionary/list structure in one go by defining serializers/deserializers for arbitrary sets of classes.

Tested with python3.

Serializer can be utilized either as instantiated or non-instantiated.

## Install

`pip3 install anserializer`


## Examples

### Instantiated example
```
from anserializer import Serializer, DatetimeSerializer, ObjectSerializer

class MyObjectClass(object):
  pass

# instantiate the serializer
s  = s = Serializer([ DatetimeSerializer(), ObjectSerializer(MyObjectClass) ])

# create object
o = MyObjectClass()
print(o)

# serialize object
x = s.get_serialized(o)
print(x)

# deserialize object
o = s.get_deserialized(x)
print(o)
```

### Non-instantiated example
```
from anserializer import Serializer, DatetimeSerializer, ObjectSerializer

class MyObjectClass(object):
  pass

# put our list of serializer classes available for use into a variable
serializers = [ DatetimeSerializer(), ObjectSerializer(MyObjectClass) ]

# create object
o = MyObjectClass()
print(o)

# serialize object
x = Serializer.serialize(o, serializers)
print(x)

# deserialize object
o = Serializer.deserialize(x, serializers)
print(o)
```

### Allow children to be serialized by a serializer defined for their ancestor
```
from anserializer import Serializer, DatetimeSerializer, ObjectSerializer

class MyObjectClass(object):
  pass

# instantiate the serializer
s  = s = Serializer([ DatetimeSerializer(), ObjectSerializer(object) ], serialize_children=True)

# create object
o = MyObjectClass()
print(o)

# serialize object
x = s.get_serialized(o)
print(x)
```

### Use your own serializer
```
from anserializer import Serializer, DatetimeSerializer, ObjectSerializer, BaseSerializer

class MyObjectClass(object):
  pass

# create your serializer
class MySerializer(BaseSerializer):
  def __init__(self):
    super().__init__([MyObjectClass], '^!MyObjectClass\(\)$')

  def serialize(self, obj):
    # do the magic and return a serialized element 
    return { '!MyObjectClass()': { 
         # insert object data here
      }
    }

  def deserialize(self, serialized_obj):
    # do the magic and return an object with the data given in serialized format
    kwargs = {}
    return MyObjectClass(**kwargs)

# instantiate the serializer
s = Serializer([ DatetimeSerializer(), MySerializer(), ObjectSerializer(object) ])

# create object
o = MyObjectClass()
print(o)

# serialize object
x = s.get_serialized(o)
print(x)
```

Serializer([ serializer.DatetimeSerializer(), serializer.ObjectSerializer(object), serializer.MySerializer(MyClass) ])
