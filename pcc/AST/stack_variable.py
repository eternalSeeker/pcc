class StackVariable:
    def __init__(self, name, size, initializer_byte_array, type_name):
        self.name = name
        self.size = size
        self.initializer_byte_array = initializer_byte_array
        self.stack_offset = 0
        self.stack_start = 0
        self.type_name = type_name
