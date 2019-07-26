from pcc.AST.compiled_object import CompiledObjectType, CompiledObject
from pcc.AST.statement import Statement
from pcc.compiler.assembler import ProcessorRegister


class ReturnStatement(Statement):

    def __init__(self, depth, identifier, constant):
        """Create a return statement.

        Args:
            depth (int): depth in the ast tree
            identifier (str): the identifier of the symbol to return if
                              applicable
            constant (pcc.AST.constant_expression.ConstantExpression):
                the constant expression to return if applicable
        """
        super(ReturnStatement, self).__init__(depth)
        self.id = identifier
        self.constant = constant

    def __str__(self):
        string = self._depth * '  ' + 'Return: \n'
        if self.id:
            string += self._depth * '  ' + '  ID: %s\n' % self.id
        if self.constant:
            string += '%s\n' % str(self.constant)
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
            assembler (Assembler)
        Returns:
            CompiledObject: the compiled version of this statement
        """
        value = bytearray()

        if self.constant:
            try:
                imm_value = int(self.constant.exp_value)
                reg = ProcessorRegister.accumulator
                value += assembler.copy_value_to_reg(imm_value, reg)
            except ValueError:
                imm_value = float(self.constant.exp_value)
                return_type = self.get_return_type()
                if return_type == 'double':
                    reg = ProcessorRegister.double_scalar_0
                else:
                    reg = ProcessorRegister.single_scalar_0
                value += assembler.copy_value_to_reg(imm_value, reg)
        elif self.id:
            return_type = self.get_return_type()
            if return_type == 'double':
                reg = ProcessorRegister.double_scalar_0
            elif return_type == 'float':
                reg = ProcessorRegister.single_scalar_0
            else:
                reg = ProcessorRegister.accumulator

            parent = self.parent_node
            id = self.id
            stack_variable = parent.get_stack_variable(id)
            stack_offset = stack_variable.stack_offset

            value += assembler.copy_stack_to_reg(stack_offset, reg)

        # restore the frame pointer from stack
        ret = assembler.pop_from_stack(ProcessorRegister.base_pointer)
        value.extend(ret)

        # return to the called function
        ret = assembler.return_to_caller()
        value.extend(ret)

        size = len(value)
        compiled_object = CompiledObject(self.id, size,
                                         value, CompiledObjectType.code)
        return compiled_object
