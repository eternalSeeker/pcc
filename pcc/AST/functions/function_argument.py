from pcc.AST.statement import Statement


class FunctionArgument(Statement):

    def __init__(self, type_name, type_decl, identifier, depth):
        super(FunctionArgument, self).__init__(depth)
        self.type_name = type_name
        self.type_decl = type_decl
        self.identifier = identifier

    def __str__(self):
        string = ''
        string += self._depth * '  ' + 'Typename: ' \
            + str(self.type_name) + ', []\n'
        string += self._depth * '  ' + '  TypeDecl: ' \
            + str(self.type_decl) + ', []\n'
        string += self._depth * '  ' + '    IdentifierType: [\'' \
            + str(self.identifier) + '\']\n'
        return string
