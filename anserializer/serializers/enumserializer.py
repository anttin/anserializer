from .baseserializer import BaseSerializer


class EnumSerializer(BaseSerializer):

    def __init__(self, enum_class_list):
        super().__init__(enum_class_list, '^!Enum\(\)$')

        self._enum_lookup = {}
        for x in enum_class_list:
            self._enum_lookup[x.__name__] = x

    def serialize(self, obj):
        from enum import Enum, EnumMeta
        if isinstance(obj, (Enum, EnumMeta)) and type(obj).__name__ in self._enum_lookup.keys():
            return {'!Enum()': str(obj)}
        else:
            raise Exception(
                "Unknown Enum ({}), unwilling to serialize".format(type(obj)))

    def deserialize(self, serialized_obj):
        name, member = serialized_obj['!Enum()'].split('.')
        if name not in self._enum_lookup:
            raise Exception("Unknown Enum, unwilling to deserialize")

        enum_cls = self._enum_lookup[name]

        return getattr(enum_cls, member)
