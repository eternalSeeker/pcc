from pcc.AST.compiled_object import CompiledObjectType, CompiledObject
from pcc.AST.statement import Statement
from pcc.compiler.assembler import ProcessorRegister


class Assignment(Statement):

    def __init__(self, depth, identifier, initializer_exp):
        """Create an assignment.

        Args:
            depth (int): the depth in the tree
            identifier (str): the variable to assign to
            initializer_exp (Expression): the expression as right hand value
        """
        super(Statement, self).__init__(depth)
        self.id = identifier
        self.initializer_exp = initializer_exp

    def __str__(self):
        string = self._depth * '  ' + 'Assignment: =\n'
        string += self._depth * '  ' + '  ID: %s\n' % self.id
        string += self._depth * '  ' + str(self.initializer_exp)
        string += '\n'
        return string

    def compile(self, assembler):
        """Compile this statement

        Args:
            assembler (Assembler)
        Returns:
            CompiledObject: the compiled version of this statement
        """
        value = bytearray()

        parent = self.parent_node
        id = self.id
        stack_variable = parent.get_stack_variable(id)
        stack_offset = stack_variable.stack_offset
        size = stack_variable.size

        if stack_variable.type_name == 'double':
            register = ProcessorRegister.double_scalar_0
        elif stack_variable.type_name == 'float':
            register = ProcessorRegister.single_scalar_0
        else:
            register = ProcessorRegister.accumulator

        value += self.initializer_exp.load_result_to_reg(register, assembler)

        value += assembler.copy_reg_to_stack(stack_offset, register)
        compiled_object = CompiledObject(self.id, size,
                                         value, CompiledObjectType.code)
        return compiled_object
