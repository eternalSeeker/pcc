from pcc.AST.binary_operator import BinaryOperator


class BitwiseAnd(BinaryOperator):
    def __init__(self, depth, operand_1, operand_2):
        super(BitwiseAnd, self).__init__(depth, operand_1, operand_2)
        self.operator = '&'

    def evaluate(self, source, destination, assembler):
        """Evaluate the operator, leaving the result in the destination reg.

        Args:
            source (ProcessorRegister): the source operand
            destination (ProcessorRegister): the destination operand
            assembler (Assembler): the assembler to use

        Returns:
            bytearray: the byte code
        """
        value = bytearray()
        value += assembler.bitwise_and(source, destination)
        return value
