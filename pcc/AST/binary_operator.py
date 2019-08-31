from pcc.AST.expression import Expression
from pcc.compiler.assembler import ProcessorRegister


class BinaryOperator(Expression):

    def __init__(self, depth, operand_1, operand_2):
        """Create a binary operator

        Args:
            depth (int): the depth in the tree
            operand_1 (Expression): the first operand
            operand_2 (Expression): the second operand
        """
        super(BinaryOperator, self).__init__(depth)
        self.operator = None
        self.operand_1 = operand_1
        self.operand_2 = operand_2

    def __str__(self):
        string = (self._depth + 1) * '  ' + 'BinaryOp: %s\n' % self.operator
        string += '  ' + '%s\n' % self.operand_1
        string += '  ' + '%s' % self.operand_2
        return string

    def evaluate(self, source, destination, assembler):
        """Evaluate the operator, leaving the result in the destination reg.

        Args:
            source (ProcessorRegister): the source operand
            destination (ProcessorRegister): the destination operand
            assembler (Assembler): the assembler to use

        Returns:
            bytearray: the byte code # noqa I202

        Raises:
            NotImplementedError: if not implemented in a subclass
        """
        raise NotImplementedError

    def load_result_to_reg(self, register, assembler):
        """Load the result of the expression to the specified register

        Args:
            register (ProcessorRegister): the register to load the result
            assembler (Assembler): the assembler to use

        Returns:
            bytearray: the compiled code to evaluate the expression

        """
        if register == ProcessorRegister.single_scalar_0:
            register_1 = ProcessorRegister.single_scalar_0
            register_2 = ProcessorRegister.single_scalar_1
        elif register == ProcessorRegister.double_scalar_0:
            register_1 = ProcessorRegister.double_scalar_0
            register_2 = ProcessorRegister.double_scalar_1
        else:
            register_1 = ProcessorRegister.accumulator
            register_2 = ProcessorRegister.counter
        value = self.operand_1.load_result_to_reg(register_1, assembler)

        value += self.operand_2.load_result_to_reg(register_2, assembler)

        value += self.evaluate(source=register_2,
                               destination=register_1,
                               assembler=assembler)

        # the result is in register_1, make sure
        # that is the specified register
        if register != register_1:
            value += assembler.copy_from_reg_to_reg(register_1, register)

        return value
