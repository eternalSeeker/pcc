
class Statement:

    def __init__(self):
        pass

    def to_string(self):
        return 'Unknown'


class VariableDeclaration(Statement):

    def __init__(self, type, name, initializer):
        super(VariableDeclaration, self).__init__()
        self.type = type
        self.name = name
        self.initializer = initializer

    def to_string(self):
        string = '  Decl: ' + self.name + ', [], [], []\n'
        string += '    TypeDecl: ' + self.name + ', []\n'
        string += '      IdentifierType: [\'' + self.type + '\']\n'
        if self.initializer:
            string += '    Constant: ' + self.type + ', ' + self.initializer \
                      + '\n'
        return string


class AstNode:

    def __init__(self, parent_node):
        self.statement_sequence = []
        self.parent_node = parent_node

    def add_statement(self, statement):
        self.statement_sequence.append(statement)


class Ast:

    c_types = ['int', 'char', 'float', 'double']

    def __init__(self, source_code):
        self.source_code = source_code
        self.is_completed = False
        self.types = Ast.c_types
        self.root_node = AstNode(None)
        self.current_node = self.root_node
        self.source_code_list = []
        self.index = 0

    def run_ast(self):
        self.source_code_list = self.source_code.split('\n')
        while self.index != len(self.source_code_list):
            self.read_next_statement()

        return 0

    def read_initializer(self, args):
        if args:
            return args[0]
        return None

    def read_variable(self, statement):
        list_of_tokens = statement.split()
        variable_type = None
        identifier = None
        operand = None
        if list_of_tokens[0] in self.types:
            variable_type = list_of_tokens[0]
            identifier = list_of_tokens[1]
        if len(list_of_tokens) > 2:
            if list_of_tokens[2] == '=':
                operand = self.read_initializer(list_of_tokens[3:])
        if identifier:
            statement = VariableDeclaration(variable_type, identifier, operand)
            self.current_node.add_statement(statement)

    def read_next_statement(self):
        line = self.source_code_list[self.index]
        if ';' in line:
            statement = line.split(';')[0]
            self.read_variable(statement)
        self.index += 1

    def to_string(self):
        string = 'FileAST: \n'
        for element in self.root_node.statement_sequence:
            string += element.to_string()

        return string
