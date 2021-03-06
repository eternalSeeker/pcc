from pcc.AST.compiled_object import CompiledObjectType, CompiledObject
from pcc.AST.statement import Statement
from pcc.AST.expression import Expression


class CompoundStatement(Statement):

    def __init__(self, depth):
        super(CompoundStatement, self).__init__(depth)

    def __str__(self):
        string = self._depth * '  ' + 'Compound: \n'
        for arg in self.statement_sequence:
            string += str(arg)
            if isinstance(arg, Expression):
                string += '\n'
        return string

    def get_return_type(self):
        """Get the return type.

        Returns:
            str: the return type
        """
        return self.parent_node.get_return_type()

    def compile(self, assembler):
        """Compile this statement

        Args:
            assembler (Assembler): the assembler to use

        Returns:
            CompiledObject: the compiled version of this statement
        """
        value = bytearray()
        relocation_objects = []
        for statement in self.statement_sequence:
            compiled_object = statement.compile(assembler)
            if compiled_object is None:
                continue
            reloc_objects = compiled_object.relocation_objects
            for relocation_object in reloc_objects:
                additional_offset = len(value)
                relocation_object.offset += additional_offset
                relocation_objects.append(relocation_object)
            value += compiled_object.value

        size = len(value)
        compiled_object = CompiledObject('compoundStatement', size,
                                         value, CompiledObjectType.code,
                                         relocation_objects)
        return compiled_object

    def add_stack_variable(self, current_list):
        """Add all stack variable to the list

        Args:
            current_list(list[StackVariable]): the current list
        """
        for statement in self.statement_sequence:
            statement.add_stack_variable(current_list)

    def get_stack_variable(self, variable_name):
        """Get the stack variable by name.

        Args:
            variable_name (str): the name of the variable

        Returns:
            StackVariable: the stack variable if found, else None
        """
        return self.parent_node.get_stack_variable(variable_name)
