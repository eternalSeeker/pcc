import enum


class CompiledObjectType(enum.Enum):
    data = 1,
    code = 2,


class CompiledObject:

    def __init__(self, name, size, value, object_type):
        """Create an compiled object.

        Args:
            name (str): the name of the object
            size (int): the size of the object
            value (bytearray): the content of the object
            object_type (CompiledObjectType): the type of object

        """
        self.name = name
        self.size = size
        self.value = value
        self.type = object_type
