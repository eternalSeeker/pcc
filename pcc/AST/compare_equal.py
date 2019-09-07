from pcc.AST.binary_operator import BinaryOperator


class CompareEqual(BinaryOperator):
    def __init__(self, depth, operand_1, operand_2):
        super(CompareEqual, self).__init__(depth, operand_1, operand_2)
        self.operator = '=='

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
        cmp_values = assembler.cmp(source, destination)
        clear_result = assembler.copy_value_to_reg(0, destination)
        set_result = assembler.copy_value_to_reg(1, destination)
        jump_amount = len(set_result)
        jump_over_set_result = assembler.jne(jump_amount)

        # compare the 2 value, clean the destination and if the 2 values
        # were equal, set the result, else jump over these instructions
        value += cmp_values
        value += clear_result
        value += jump_over_set_result
        value += set_result

        return value
