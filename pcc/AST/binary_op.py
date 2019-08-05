from pcc.AST.expression import Expression
from pcc.compiler.assembler import ProcessorRegister


class BinaryOp(Expression):

    def __init__(self, depth, operator, operand_1, operand_2):
        """Create a binary operator

        Args:
            depth (int): the depth in the tree
            operator (pcc.AST.binary_operator.BinaryOperator): the operator
            operand_1 (Expression): the first operand
            operand_2 (Expression): the second operand
        """
        super(BinaryOp, self).__init__(depth)
        self.operator = operator
        self.operand_1 = operand_1
        self.operand_2 = operand_2

    def __str__(self):
        string = (self._depth + 1) * '  ' + 'BinaryOp: %s\n' % self.operator
        string += '  ' + '%s\n' % self.operand_1
        string += '  ' + '%s' % self.operand_2
        return string

    def load_result_to_reg(self, register, assembler):
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

        value += self.operator.evaluate(source=register_2,
                                        destination=register_1,
                                        assembler=assembler)

        # the result is in register_1, make sure
        # that is the specified register
        if register != register_1:
            value += assembler.copy_from_reg_to_reg(register_1, register)

        return value
