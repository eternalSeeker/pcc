from pcc.AST.expression import Expression


class VariableReference(Expression):

    def __init__(self, depth, name):
        """Create a expression that references a variable

        Args:
            depth (int): the depth in the tree
            name (str): the name of the variable
        """
        super(VariableReference, self).__init__(depth)
        self.name = name

    def __str__(self):
        string = self._depth * '  ' + 'ID: %s\n' % self.name
        return string

    def load_result_to_reg(self, register, assembler):
        """Load the result of the expression to the specified register

        Args:
            register (ProcessorRegister): the register to load the result
            assembler (Assembler): the assembler to use
        Returns:
            bytearray: the compiled code to evaluate the expression
        """
        pass
