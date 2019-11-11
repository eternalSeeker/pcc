from pcc.AST.ast_node import AstNode


class Expression(AstNode):
    def __init__(self, depth):
        super(Expression, self).__init__(depth)

    def __str__(self):
        string = self._depth * '  ' + 'This is an expression\n'
        return string

    def load_result_to_reg(self, register, assembler):
        """Load the result of the expression to the specified register

        Args:
            register (ProcessorRegister): the register to load the result
            assembler (Assembler): the assembler to use

        Returns:
            bytearray: the compiled code to evaluate the expression # noqa I202
            List[RelocationObject]: the required relocation objects

        Raises:
            NotImplementedError: if not implemented in a subclass
        """
        raise NotImplementedError
