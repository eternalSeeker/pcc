from pcc.AST.compiled_object import CompiledObjectType, CompiledObject
from pcc.AST.statement import Statement
from pcc.compiler.assembler import ProcessorRegister


class ReturnStatement(Statement):

    def __init__(self, depth, expression):
        """Create a return statement.

        Args:
            depth (int): depth in the ast tree
            expression (Union[pcc.AST.expression.Expression, None]): the
                expression to return if applicable
        """
        super(ReturnStatement, self).__init__(depth)
        self.expression = expression

    def __str__(self):
        string = self._depth * '  ' + 'Return: \n'
        if self.expression:
            string += '%s\n' % str(self.expression)
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

        if self.expression:
            return_type = self.get_return_type()
            if return_type == 'double':
                reg = ProcessorRegister.double_scalar_0
            elif return_type == 'float':
                reg = ProcessorRegister.single_scalar_0
            else:
                reg = ProcessorRegister.accumulator
            compiled_code, rela_objects = \
                self.expression.load_result_to_reg(reg, assembler)
            value += compiled_code
        else:
            rela_objects = []

        # set the base pointer as the new stack pointer
        src = ProcessorRegister.base_pointer
        dest = ProcessorRegister.frame_pointer
        ret = assembler.copy_from_reg_to_reg(destination=dest,
                                             source=src)
        value.extend(ret)

        # restore the frame pointer from stack
        ret = assembler.pop_from_stack(ProcessorRegister.base_pointer)
        value.extend(ret)

        # return to the called function
        ret = assembler.return_to_caller()
        value.extend(ret)

        size = len(value)
        compiled_object = CompiledObject(self.expression, size,
                                         value, CompiledObjectType.code,
                                         rela_objects)
        return compiled_object
