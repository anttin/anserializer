# anserializer

A simple serializer mechanism for serializing and deserializing simple and complex data structures to/from json. It allows the user to simply deserialize a complex dictionary/list structure in one go by defining serializers/deserializers for arbitrary sets of classes.

Tested with python3.

Serializer can be utilized either as instantiated or non-instantiated.


## Instantiated example
```
s = serializer.Serializer([ serializer.DatetimeSerializer(), serializer.ObjectSerializer(object), serializer.MySerializer(MyClass) ])
x = ser.get_serialized(o)
_x = ser.get_deserialized(x)
```

## Non-instantiated example
```
serializers = [ serializer.DatetimeSerializer(), serializer.ObjectSerializer(object), serializer.MySerializer(MyClass) ]
x = serializer.Serializer.serialize(o, serializers)
_x = serializer.Serializer.deserialize(x, serializers)
```
