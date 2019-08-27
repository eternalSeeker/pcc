from pcc.AST.operator import Operator


class UnaryOperator(Operator):
    def __init__(self):
        super(UnaryOperator, self).__init__()

    def __str__(self):
        return ''

    def evaluate(self, destination, assembler):
        """Evaluate the operator, leaving the result in the destination reg.

        Args:
            destination (ProcessorRegister): the destination operand
            assembler (Assembler): the assembler to use

        Returns:
            bytearray: the byte code # noqa I202

        Raises:
            NotImplementedError: if not implemented in a subclass
        """
        raise NotImplementedError
