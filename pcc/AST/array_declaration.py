from pcc.AST.statement import Statement


class ArrayDeclaration(Statement):

    def __init__(self, variable_type, name, initializer, initializer_type,
                 array_size, array_size_type, depth):
        super(ArrayDeclaration, self).__init__(depth)
        self.variable_type = variable_type
        self.name = name
        self.initializer = initializer
        self.initializer_type = initializer_type
        self.array_size = array_size
        self.array_size_type = array_size_type

    def __str__(self):
        string = self._depth * '  ' + 'Decl: ' + self.name + ', [], [], []\n'
        string += self._depth * '  ' + '  ArrayDecl: []\n'
        string += self._depth * '  ' + '    TypeDecl: ' + self.name + ', []\n'
        string += self._depth * '  ' + '      IdentifierType: [\'' \
            + self.variable_type.name + '\']\n'
        if self.array_size:
            string += self._depth * '  ' + '    Constant: ' + \
                      self.array_size_type + ', ' + \
                      self.array_size + '\n'
        if self.initializer:
            string += self._depth * '  ' + '  Constant: ' + \
                      self.initializer_type + ', ' + \
                      self.initializer + '\n'
        return string
