class BaseSerializer(object):
    def __init__(self, obj_types, id_regex):
        if isinstance(obj_types, list):
            self._obj_types = obj_types
        else:
            self._obj_types = [obj_types]

        self.id_regex = id_regex

    def get_obj_type_dict(self):
        types = {}
        for _type in self._obj_types:
            types[_type] = self
        return types

    def get_id_regex_dict(self):
        return {self.id_regex: self}

    # override this to return serialization from object

    def serialize(self, obj):
        raise Exception("Custom serializer does not override serialize()")

    # override this to return deserialized object

    def deserialize(self, serialized_obj):
        raise Exception("Custom serializer does not override deserialize()")
