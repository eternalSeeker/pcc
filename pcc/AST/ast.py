from pcc.utils.stringParsing import extractTextForEnclosedParenthesis


class Statement:

    def __init__(self):
        pass

    def __str__(self):
        return 'Unknown'


class VariableDeclaration(Statement):

    def __init__(self, type, name, initializer, initializer_type):
        super(VariableDeclaration, self).__init__()
        self.type = type
        self.name = name
        self.initializer = initializer
        self.initializer_type = initializer_type

    def __str__(self):
        string = '  Decl: ' + self.name + ', [], [], []\n'
        string += '    TypeDecl: ' + self.name + ', []\n'
        string += '      IdentifierType: [\'' + self.type + '\']\n'
        if self.initializer:
            string += '    Constant: ' + \
                      self.initializer_type + ', ' + \
                      self.initializer + '\n'
        return string


class FunctionArgument:

    def __init__(self, type_name, type_decl, identifier):
        self.type_name = type_name
        self.type_decl = type_decl
        self.identifier = identifier


class FunctionDeclaration(Statement):

        def __init__(self, return_type, name, argument_list):
            super(FunctionDeclaration, self).__init__()
            self.return_type = return_type
            self.name = name
            self.argument_list = argument_list

        def __str__(self):
            string = '  Decl: ' + self.name + ', [], [], []\n'
            string += '    FuncDecl: \n'
            string += '      ParamList: \n'
            for arg in self.argument_list:
                string += '        Typename: ' + str(arg.type_name) + ', []\n'
                string += '          TypeDecl: ' +\
                          str(arg.type_decl) + ', []\n'
                string += '            IdentifierType: [\'' + \
                          str(arg.identifier) + '\']\n'
            string += '      TypeDecl: ' + self.name + ', []\n'
            string += '        IdentifierType: [\'' +\
                      self.return_type + '\']\n'
            return string


class AstNode:

    def __init__(self, parent_node):
        self.statement_sequence = []
        self.parent_node = parent_node

    def add_statement(self, statement):
        self.statement_sequence.append(statement)


class Ast:

    c_types = ['int', 'char', 'float', 'double', 'void']

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

    def get_type_of_expression(self, expression):
        type_string = None
        try:
            int(expression, 0)
            type_string = 'int'
            return type_string
        except ValueError:
            # it was not a number
            pass

        return type_string

    def read_variable(self, statement):
        list_of_tokens = statement.split()
        variable_type = None
        if list_of_tokens[0] in self.types:
            variable_type = list_of_tokens[0]
        if variable_type:
            declarations = statement.replace(variable_type + ' ', '')
            list_of_declarations = declarations.split(',')
            for declaration in list_of_declarations:
                if '=' in declaration:
                    parts = declaration.split('=')
                    identifier = parts[0]
                    initializer = parts[1]
                    # remove all whitespace chars from initializer
                    initializer = ''.join(initializer.split())
                    initializer_type = self.get_type_of_expression(initializer)
                else:
                    identifier = declaration
                    initializer = None
                    initializer_type = None
                # remove all whitespace chars from identifier
                identifier = ''.join(identifier.split())
                if '(' in identifier:
                    # there cannnot be a parentesis in the variable name,
                    # this is probably a function
                    return
                statement = VariableDeclaration(variable_type,
                                                identifier,
                                                initializer,
                                                initializer_type)
                self.current_node.add_statement(statement)

    def read_function_declaration(self, statement):
        list_of_tokens = statement.split()
        if list_of_tokens[0] in self.types:
            return_type = list_of_tokens[0]
            name_start = statement.index(list_of_tokens[1])
            if '(' not in statement:
                # not a function declaration
                return
            arg_list_start = statement.index('(')
            function_name = statement[name_start: arg_list_start]
            argument_list = \
                extractTextForEnclosedParenthesis(statement, arg_list_start)
            list_of_args = argument_list.split(',')
            function_arguments = []
            for arg in list_of_args:
                parts = arg.split()
                arg_type = parts[0]
                if arg_type != 'void':
                    arg_name = parts[1]
                else:
                    arg_name = arg_type
                    arg_type = None
                funct_arg = FunctionArgument(arg_type, None, arg_name)
                function_arguments.append(funct_arg)
            function_declaration = \
                FunctionDeclaration(return_type, function_name,
                                    function_arguments)
            self.current_node.add_statement(function_declaration)

    def read_next_statement(self):
        line = self.source_code_list[self.index]
        if ';' in line:
            statement = line.split(';')[0]
            self.read_variable(statement)
            self.read_function_declaration(statement)
        self.index += 1

    def to_string(self):
        string = 'FileAST: \n'
        for element in self.root_node.statement_sequence:
            string += element.__str__()

        return string
