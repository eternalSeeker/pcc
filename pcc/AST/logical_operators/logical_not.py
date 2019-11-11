from pcc.AST.unary_operator import UnaryOperator
from pcc.compiler.assembler import ProcessorRegister


class LogicalNot(UnaryOperator):
    def __init__(self, depth, operand):
        """Create a binary operator

        Args:
            depth (int): the depth in the tree
            operand (Expression): the operand
        """
        super(LogicalNot, self).__init__(depth, operand)
        self.operator = '!'

    def evaluate(self, destination, assembler):
        """Evaluate the operator, leaving the result in the destination reg.

        Args:
            destination (ProcessorRegister): the destination operand
            assembler (Assembler): the assembler to use

        Returns:
            bytearray: the byte code
        """
        value = bytearray()
        value += assembler.logical_not(destination)
        return value

    def load_result_to_reg(self, register, assembler):
        """Load the result of the logical not to the specified register

        Args:
            register (ProcessorRegister): the register to load the result
            assembler (Assembler): the assembler to use

        Returns:
            bytearray: the compiled code to evaluate the expression
            List[RelocationObject]: the required relocation objects
        """
        value = bytearray()
        if register != ProcessorRegister.accumulator:
            register_1 = ProcessorRegister.accumulator
        else:
            register_1 = ProcessorRegister.counter
        clear_result = assembler.copy_value_to_reg(0, register)
        set_result = assembler.copy_value_to_reg(1, register)
        if_instructions, relocation_objects = \
            self.operand.load_result_to_reg(register_1, assembler)
        if_instructions += assembler.cmp_against_const(register_1, 0)

        jump_amount = len(set_result)
        if_instructions += assembler.jne(jump_amount)

        value += clear_result

        for rela_obj in relocation_objects:
            additional_offset = len(clear_result)
            rela_obj.offset += additional_offset

        value += if_instructions
        value += set_result

        return value, relocation_objects
