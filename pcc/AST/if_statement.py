from pcc.AST.compiled_object import CompiledObjectType, CompiledObject
from pcc.AST.statement import Statement


class IfStatement(Statement):

    def __init__(self, depth, condition, if_statement, else_statement=None):
        """Create an if statement.

        Args:
            depth (int): depth in the ast tree
            condition (pcc.AST.expression.Expression): the conditional to
                evaluate to true to jump to the if branch else the else
            if_statement (pcc.AST.Statement): the if branch
            else_statement (Union[pcc.AST.Statement, None]): the if branch
        """
        super(IfStatement, self).__init__(depth)
        self.condition = condition
        self.if_statement = if_statement
        self.else_statement = else_statement

    def __str__(self):
        string = self._depth * '  ' + 'If: \n'
        string += '%s\n' % str(self.condition)
        string += '%s' % str(self.if_statement)
        if self.else_statement:
            string += '%s' % str(self.else_statement)
        return string

    def compile(self, assembler):
        """Compile this statement

        Args:
            assembler (Assembler)
        Returns:
            CompiledObject: the compiled version of this statement
        """
        value = bytearray()

        size = len(value)
        compiled_object = CompiledObject('if', size,
                                         value, CompiledObjectType.code)
        return compiled_object
