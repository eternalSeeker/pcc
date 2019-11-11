from pcc.AST.binary_operator import BinaryOperator
from pcc.compiler.assembler import ProcessorRegister


class LogicalAnd(BinaryOperator):
    def __init__(self, depth, operand_1, operand_2):
        super(LogicalAnd, self).__init__(depth, operand_1, operand_2)
        self.operator = '&&'

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
        value += assembler.logical_and(source, destination)
        return value

    def load_result_to_reg(self, register, assembler):
        """Load the result of the logical and to the specified register

        Args:
            register (ProcessorRegister): the register to load the result
            assembler (Assembler): the assembler to use

        Returns:
            bytearray: the compiled code to evaluate the expression
            List[RelocationObject]: the required relocation objects

        """
        value = bytearray()
        relocation_objects = []
        if register != ProcessorRegister.accumulator:
            register_1 = ProcessorRegister.accumulator
        else:
            register_1 = ProcessorRegister.counter
        clear_result = assembler.copy_value_to_reg(0, register)
        set_result = assembler.copy_value_to_reg(1, register)
        if_instructions, rela_objects_if = \
            self.operand_1.load_result_to_reg(register_1, assembler)
        for rela_obj in rela_objects_if:
            additional_offset = len(clear_result)
            rela_obj.offset += additional_offset
            relocation_objects.append(rela_obj)
        if_instructions += assembler.cmp_against_const(register_1, 0)

        else_instructions, rela_objects_else = \
            self.operand_2.load_result_to_reg(register_1, assembler)
        for rela_obj in rela_objects_else:
            additional_offset = len(clear_result + if_instructions)
            rela_obj.offset += additional_offset
            relocation_objects.append(rela_obj)
        else_instructions += assembler.cmp_against_const(register_1, 0)
        jump_amount = len(set_result)
        else_instructions += assembler.je(jump_amount)

        jump_amount = len(else_instructions) + len(set_result)
        if_instructions += assembler.je(jump_amount)

        value += clear_result
        value += if_instructions
        value += else_instructions
        value += set_result

        return value, relocation_objects
