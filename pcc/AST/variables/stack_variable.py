
class StackVariable:
    def __init__(self, name, size, initializer_byte_array, type_name):
        """Create a stack variable.

        Args:
            name (str): the name of the variable
            size (int): the size in bytes
            initializer_byte_array (bytearray): the initializer
            type_name (VariableType): the variable
        """
        self.name = name
        self.size = size
        self.initializer_byte_array = initializer_byte_array
        self.stack_offset = 0
        self.stack_start = 0
        self.type_name = type_name

    def __str__(self):
        string = 'Stack variable: '
        string += f'name {self.name}, size {self.size} '
        string += f'type {str(self.type_name)} '
        return string
