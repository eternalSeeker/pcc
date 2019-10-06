from pcc.AST.expression import Expression


class FunctionCall(Expression):

    def __init__(self, depth, identifier, expression_list=None):
        super(FunctionCall, self).__init__(depth)
        if expression_list is None:
            expression_list = []
        self.id = identifier
        self.expression_list = expression_list

    def __str__(self):
        string = self._depth * '  ' + 'FuncCall: \n'
        string += self._depth * '  ' + '  ID: %s\n' % self.id
        if self.expression_list:
            string += self._depth * '  ' + '  ExprList: \n'
            for expression in self.expression_list:
                string += "%s\n" % str(expression)
        index = string.rfind('\n')
        string = string[:index] + string[index+1:]
        return string

    def load_result_to_reg(self, register, assembler):
        pass