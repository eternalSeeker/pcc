import enum


class CompiledObjectType(enum.Enum):
    none_type = 0,
    data = 1,
    code = 2,


class CompiledObject:

    def __init__(self, name, size, value, object_type, relocation_objects=[]):
        """Create an compiled object.

        Args:
            name (str): the name of the object
            size (int): the size of the object
            value (bytearray): the content of the object
            object_type (CompiledObjectType): the type of object
            relocation_objects (List[RelocationObject]): the used
                relocation objects

        """
        self.name = name
        self.size = size
        self.value = value
        self.type = object_type
        self.relocation_objects = relocation_objects
