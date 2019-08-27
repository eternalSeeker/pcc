from pcc.AST.binary_operator import BinaryOperator


class BitwiseXor(BinaryOperator):
    def __init__(self):
        super(BitwiseXor, self).__init__()

    def __str__(self):
        return '^'

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
        value += assembler.bitwise_xor(source, destination)
        return value
