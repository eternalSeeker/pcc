from pcc.AST.expression import Expression
from pcc.compiler.assembler import ProcessorRegister


class ConstantExpression(Expression):
    def __init__(self, exp_type, expr_value, depth):
        super(ConstantExpression, self).__init__(depth)
        self.exp_type = exp_type
        self.exp_value = expr_value

    def __str__(self):
        string = (self._depth + 1) * '  ' + \
                 'Constant: %s, %s' % (self.exp_type, self.exp_value)
        return string

    def load_result_to_reg(self, register, assembler):
        """Load the result of the expression to the specified register

        Args:
            register (ProcessorRegister): the register to load the result
            assembler (Assembler): the assembler to use

        Returns:
            bytearray: the compiled code to evaluate the expression
        """
        if register == ProcessorRegister.double_scalar_0 or \
                register == ProcessorRegister.double_scalar_1:
            val = float(self.exp_value)
        elif register == ProcessorRegister.single_scalar_0 or \
                register == ProcessorRegister.single_scalar_1:
            val = float(self.exp_value)
        elif register == ProcessorRegister.accumulator:
            val = int(self.exp_value)
        else:
            # all other types interpreted as int
            val = int(self.exp_value)

        value = assembler.copy_value_to_reg(val, register)

        return value
