from pcc.AST.ast_node import AstNode


class Statement(AstNode):

    def __init__(self, depth):
        super(Statement, self).__init__(depth)

    def __str__(self):
        return 'Unknown'

    def get_function_definition_node(self):
        """Get the function definition if found.

        Returns:
             FunctionDefinition: the definition if found else None

        """
        return self.parent_node.get_function_definition_node()
