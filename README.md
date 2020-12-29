# anserializer

A module for serializing and deserializing complex data structures to/from json. It allows the user to (de)serialize a complex dictionary/list structure in one go by defining serializers/deserializers for arbitrary sets of classes.

Tested with python3.

Serializer can be utilized either as instantiated or non-instantiated.

## Install

`pip3 install anserializer`


## Examples

### Instantiated example
```
from anserializer import serializer

s  = anserializer.Serializer([ serializer.DatetimeSerializer(), serializer.ObjectSerializer(object), serializer.MySerializer(MyClass) ])
x  = s.get_serialized(o)
_x = s.get_deserialized(x)
```

### Non-instantiated example
```
from anserializer import serializer

serializers = [ serializer.DatetimeSerializer(), serializer.ObjectSerializer(object), serializer.MySerializer(MyClass) ]
x  = serializer.Serializer.serialize(o, serializers)
_x = serializer.Serializer.deserialize(x, serializers)
```
