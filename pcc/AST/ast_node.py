def push_variable_on_stack(assembler, stack_offset,
                           value, value_array):
    """Push a value on a specified location on stack

    Args:
        assembler (Assembler): the assembler to use
        stack_offset (int): the offset relative to the current stack pointer
        value (bytearray): the byte array to append the machine code to
        value_array (bytearray): the bytearray to push to stack

    Returns:
        bytearray: the array with the added machine code
        int: the stackoffset
    """

    number_of_words = int((len(value_array) - 1) / 4) + 1
    for i in range(number_of_words):
        part_of_array = value_array[i * 4:(i + 1) * 4]
        stack_offset -= 4
        value += assembler.push_value_to_stack(part_of_array, stack_offset)

    # if multiple words are used, move the offset a word further
    if number_of_words > 1:
        stack_offset -= 4
    return value, stack_offset


class AstNode:

    def __init__(self, depth):
        self.statement_sequence = []
        self.parent_node = None
        self._depth = depth

    def __str__(self):
        string = ''
        for arg in self.statement_sequence:
            string += str(arg)
        return string

    def get_function_definition_node(self):
        """Get the function definition if found.

        Returns (FunctionDefinition): the definition if found else None

        """
        return None

    def add_stack_variable(self, current_list):
        """Add all stack variable to the list.

        Args:
            current_list(list[pcc.AST.stack_variable.StackVariable]):
                the current list
        """
        pass

    def add_statement(self, statement):
        statement.parent_node = self
        self.statement_sequence.append(statement)

    def update_depth(self, depth):
        self._depth = depth
        for statement in self.statement_sequence:
            statement.update_depth(depth+1)
