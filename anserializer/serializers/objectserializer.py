from .baseserializer import BaseSerializer


class ObjectSerializer(BaseSerializer):
    def __init__(self, obj_types, class_identifiers_in_params=False):
        super().__init__(obj_types,
                         '^!Class\((([a-zA-Z_][0-9a-zA-Z_]*\.)*([a-zA-Z_][0-9a-zA-Z_]*)\.([a-zA-Z_][0-9a-zA-Z_]*))?\)$')

        self.class_identifiers_in_params = class_identifiers_in_params

    def serialize(self, obj):
        if self.class_identifiers_in_params is True:
            result = {
                '!Class()': {
                    '__module__': obj.__module__,
                    '__class__':  obj.__class__.__name__,
                    **obj.__dict__
                }
            }
        else:
            result = {'!Class({}.{})'.format(
                obj.__module__, obj.__class__.__name__, ):  {**obj.__dict__}}

        return result

    def deserialize(self, serialized_obj):
        # structure should be like this: { '!Object(Module.Class)': { ... params ... } } so only one item in the dict
        try:
            k, v = list(serialized_obj.items())[0]
        except:
            return obj

        import re
        r = re.match(self.id_regex, k)

        if not r:
            return serialized_obj

        if r.groups()[0] is None and '__class__' in v and '__module__' in v:
            module_name = v.pop("__module__")
            class_name = v.pop("__class__")
        elif r.groups()[0] is not None:
            module_name, class_name = (
                '.'.join(r.groups()[0].split('.')[:-1]),
                r.groups()[0].split('.')[-1]
            )

        module = __import__(module_name)
        cls = getattr(module, class_name)
        obj = cls(**v)

        return obj
