from pcc.AST.unary_operator import UnaryOperator


class BitwiseNot(UnaryOperator):
    def __init__(self, depth, operand):
        """Create a binary operator

        Args:
            depth (int): the depth in the tree
            operand (Expression): the operand
        """
        super(BitwiseNot, self).__init__(depth, operand)
        self.operator = '~'

    def evaluate(self, destination, assembler):
        """Evaluate the operator, leaving the result in the destination reg.

        Args:
            destination (ProcessorRegister): the destination operand
            assembler (Assembler): the assembler to use

        Returns:
            bytearray: the byte code
        """
        value = bytearray()
        value += assembler.bitwise_not(destination)
        return value
