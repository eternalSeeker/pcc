from pcc.AST.expression import Expression
from pcc.compiler.assembler import ProcessorRegister


class UnaryOp(Expression):

    def __init__(self, depth, operator, operand):
        """Create a binary operator

        Args:
            depth (int): the depth in the tree
            operator (pcc.AST.unary_operator.UnaryOperator): the operator
            operand (Expression): the operand
        """
        super(UnaryOp, self).__init__(depth)
        self.operator = operator
        self.operand = operand

    def __str__(self):
        string = (self._depth + 1) * '  ' + 'UnaryOp: %s\n' % self.operator
        string += '  ' + '%s' % self.operand
        return string

    def load_result_to_reg(self, register, assembler):
        if register == ProcessorRegister.single_scalar_0:
            register_1 = ProcessorRegister.single_scalar_0
        elif register == ProcessorRegister.double_scalar_0:
            register_1 = ProcessorRegister.double_scalar_0
        else:
            register_1 = ProcessorRegister.accumulator
        value = self.operand.load_result_to_reg(register_1, assembler)

        value += self.operator.evaluate(destination=register_1,
                                        assembler=assembler)

        # the result is in register_1, make sure
        # that is the specified register
        if register != register_1:
            value += assembler.copy_from_reg_to_reg(register_1, register)

        return value
