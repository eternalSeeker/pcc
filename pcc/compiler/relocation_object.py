

class RelocationObject:

    def __init__(self, name, offset, object_type, addend):
        """Create an compiled object.

        Args:
            name (str): the name of the object
            offset (int): the offset into the relocation object into the
                compiled code
            object_type (CompiledObjectType): the type of object
            addend (int): the addend (offset of the symbol being used)

        """
        self.name = name
        self.offset = offset
        self.symbol_index = 0
        self.type = object_type
        self.addend = addend
