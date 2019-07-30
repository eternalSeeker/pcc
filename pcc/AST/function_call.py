from pcc.AST.statement import Statement


class FunctionCall(Statement):

    def __init__(self, depth, identifier, expression_list=[]):
        super(FunctionCall, self).__init__(depth)
        self.id = identifier
        self.expression_list = expression_list

    def __str__(self):
        string = self._depth * '  ' + 'FuncCall: \n'
        string += self._depth * '  ' + '  ID: %s\n' % self.id
        if self.expression_list:
            string += self._depth * '  ' + '  ExprList: \n'
            for expression in self.expression_list:
                string += "%s\n" % str(expression)
        return string
