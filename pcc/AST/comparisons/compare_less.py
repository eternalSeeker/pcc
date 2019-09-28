from pcc.AST.binary_operator import BinaryOperator


class CompareLess(BinaryOperator):
    def __init__(self, depth, operand_1, operand_2):
        super(CompareLess, self).__init__(depth, operand_1, operand_2)
        self.operator = '<'

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

        compare = assembler.cmp(destination, source)
        clear_result = assembler.copy_value_to_reg(0, destination)
        set_result = assembler.copy_value_to_reg(1, destination)
        jump_amount = len(set_result)
        jump = assembler.jge(jump_amount)

        # compare the 2 value, clear the destination and if the destination
        # is less then source, set the result, else jump over these
        # instructions
        value += compare
        value += clear_result
        value += jump
        value += set_result

        return value
