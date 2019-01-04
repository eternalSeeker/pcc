from pcc.utils.stringParsing import extractTextForEnclosedParenthesis
from pcc.utils.stringListParsing import extract_closing_char
import pcc
import copy


class AstNode:

    def __init__(self, depth):
        self.statement_sequence = []
        self.parent_node = None
        self._depth = depth

    def __str__(self):
        string = ''
        for arg in self.statement_sequence:
            string += str(arg)
        return string

    def add_statement(self, statement):
        statement.parent_node = self
        self.statement_sequence.append(statement)

    def update_depth(self, depth):
        self._depth = depth
        for statement in self.statement_sequence:
            statement.update_depth(depth+1)


class Statement(AstNode):

    def __init__(self, depth):
        super(Statement, self).__init__(depth)

    def __str__(self):
        return 'Unknown'


class VariableDeclaration(Statement):

    def __init__(self, variable_type, name, initializer, initializer_type,
                 depth):
        super(VariableDeclaration, self).__init__(depth)
        self.variable_type = variable_type
        self.name = name
        self.initializer = initializer
        self.initializer_type = initializer_type

    def __str__(self):
        string = self._depth * '  ' + 'Decl: ' + self.name + ', [], [], []\n'
        string += self._depth * '  ' + '  TypeDecl: ' + self.name + ', []\n'
        string += self._depth * '  ' + '    IdentifierType: [\'' \
            + self.variable_type + '\']\n'
        if self.initializer:
            string += self._depth * '  ' + '  Constant: ' + \
                      self.initializer_type + ', ' + \
                      self.initializer + '\n'
        return string


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


class FunctionDeclaration(Statement):

    def __init__(self, return_type, name, argument_list, depth):
        super(FunctionDeclaration, self).__init__(depth)
        self.return_type = return_type
        self.name = name
        self.argument_list = argument_list

    def __str__(self):
        string = self._depth * '  ' + 'Decl: ' + self.name + ', [], [], []\n'
        string += self._depth * '  ' + '  FuncDecl: \n'
        string += self._depth * '  ' + '    ParamList: \n'
        for arg in self.argument_list:
            string += str(arg)
        string += self._depth * '  ' + '    TypeDecl: ' + self.name + ', []\n'
        string += self._depth * '  ' + '      IdentifierType: [\'' \
            + self.return_type + '\']\n'
        return string

    def __deepcopy__(self, memodict={}):
        return_type = self.return_type
        name = self.name
        argument_list = copy.deepcopy(self.argument_list)
        depth = self._depth
        new_copy = type(self)(return_type, name, argument_list, depth)
        return new_copy

    def update_depth(self, depth):
        super(FunctionDeclaration, self).update_depth(depth)
        for argument in self.argument_list:
            argument.update_depth(depth+3)


class FunctionDefinition(Statement):

    def __init__(self, depth):
        super(FunctionDefinition, self).__init__(depth)

    def __str__(self):
        string = self._depth * '  ' + 'FuncDef: \n'
        for arg in self.statement_sequence:
            string += str(arg)
        return string


class CompoundStatement(Statement):

    def __init__(self, depth):
        super(CompoundStatement, self).__init__(depth)

    def __str__(self):
        string = self._depth * '  ' + 'Compound: \n'
        for arg in self.statement_sequence:
            string += str(arg)
        return string


class FunctionCall(Statement):

    def __init__(self, depth, id):
        super(FunctionCall, self).__init__(depth)
        self.id = id

    def __str__(self):
        string = self._depth * '  ' + 'FuncCall: \n'
        string += self._depth * '  ' + '  ID: %s\n' % self.id
        return string


class Ast:
    c_types = ['int', 'char', 'float', 'double', 'void']

    @staticmethod
    def find_first_semicolon_in_list(list_of_source_code):
        line_number = 0
        for line in list_of_source_code:
            position = line.find(';')
            if position != -1:
                return line_number, position
            else:
                line_number += 1
        # not found
        return -1, -1

    @staticmethod
    def find_first_non_empty_in_list(list_of_source_code):
        line_number = 0
        for line in list_of_source_code:
            if line == '' or line.isspace():
                line_number += 1
            else:
                return line_number
        # not found
        return -1

    def __init__(self, source_code, file_name):
        self.source_code = source_code
        self.is_completed = False
        self.types = Ast.c_types
        self.root_node = AstNode(depth=1)
        self.current_node = self.root_node
        self.source_code_list = []
        self.index = 0
        self.filename = file_name
        self.declared_functions = []
        self.tree_string = ''

    def ast_warning(self, message):
        pcc.utils.warning.warning(self.filename,
                                  self.index, message)

    def ast_error(self, message):
        pcc.utils.warning.warning(self.filename,
                                  self.index, message)

    def get_depth_in_tree(self):
        depth = 1
        node = self.current_node
        self.tree_string = self.to_string()
        while node != self.root_node and node is not None:
            node = node.parent_node
            depth += 1
        if node is None:
            message = 'could not determine the depth of the tree for %s' % (
                self.current_node)
            self.ast_error(message)
        return depth

    def run_ast(self):
        self.source_code_list = self.source_code.split('\n')
        while self.index < len(self.source_code_list):
            self.read_next_statement()

        return 0

    @staticmethod
    def get_type_of_expression(expression):
        type_string = None
        try:
            int(expression, 0)
            type_string = 'int'
            return type_string
        except ValueError:
            # it was not a number
            pass

        return type_string

    def extract_variable_declaration_from_string(self, statement):
        list_of_tokens = statement.split()
        variable_type = None
        result_list = []
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
                    # there cannot be a parenthesis in the variable name,
                    # this is probably a function
                    return []
                # todo check if correct
                depth = self.get_depth_in_tree()
                statement = VariableDeclaration(variable_type,
                                                identifier,
                                                initializer,
                                                initializer_type,
                                                depth)
                result_list.append(statement)
        return result_list

    def read_variable(self, statements):
        line_number, statement = self.join_lines_until_next_semicolon(
            statements)
        if line_number == -1:
            return line_number
        result_list = self.extract_variable_declaration_from_string(statement)
        if not result_list:
            # no variables in the statement
            return -1
        for stat in result_list:
            self.current_node.add_statement(stat)
        return line_number

    def is_function_declared(self, function_name):
        for function_declaration in self.declared_functions:
            if function_declaration.name == function_name:
                return function_declaration
        return None

    def parse_function_definition_statement(self, function_declaration,
                                            statements):
        depth = self.get_depth_in_tree()
        function_definition = FunctionDefinition(depth)
        self.current_node.add_statement(function_definition)
        self.current_node = function_definition
        decl = copy.deepcopy(function_declaration)
        # todo access to protected member
        decl.update_depth(decl._depth+1)
        self.current_node.add_statement(decl)

        line_number = self.parse_line(statements)
        if line_number == -1:
            message = 'could not find the definition of function %s' % \
                      function_declaration.name
            self.ast_error(message)
        else:
            # the function defenition is complete go back up to its parent
            self.current_node = function_definition.parent_node
        return line_number

    def read_compound_statement(self, code_list):
        line_number = -1
        list_to_process = code_list
        open_char = '{'
        start_line = 0
        start_index = 0
        closing_char = '}'
        returned_line, returned_index = \
            extract_closing_char(list_to_process, open_char, start_line,
                                 start_index, closing_char)
        if returned_line != -1 and returned_index != -1:

            depth = self.get_depth_in_tree()
            compound_statement = CompoundStatement(depth)
            self.current_node.add_statement(compound_statement)
            self.current_node = compound_statement
            next_statements = code_list[start_line+1:returned_line]
            self.parse_line(next_statements)
            compound_statement.update_depth(depth)
            line_number = returned_line

        return line_number

    def read_function_call(self, code_list):
        line_number, statement = self.join_lines_until_next_semicolon(
            code_list)
        if line_number == -1:
            return line_number
        if '(' not in statement:
            # a function call always has an opening and closing bracket
            return -1
        splitted_statement = statement.split('(')[0]
        splitted_statement = splitted_statement.split()
        for part in splitted_statement:
            if self.is_function_declared(part):
                function_name = part
                start_index = statement.index('(')
                arguments = extractTextForEnclosedParenthesis(statement,
                                                              start_index)
                if arguments == '' or arguments.isspace():
                    depth = self.get_depth_in_tree()
                    function_call = FunctionCall(depth, function_name)
                    self.current_node.add_statement(function_call)
                else:
                    # todo parse arguments
                    pass
        return line_number

    def read_function_definition(self, statements):
        found = False
        for line in statements:
            if '{' in line:
                pass
        line_number, statement = self.join_lines_until_next_non_empty_line(
            statements)
        if line_number == -1:
            return line_number
        list_of_tokens = statement.split()

        for token in list_of_tokens:
            if '(' in token:
                token = token.split('(')[0]
            function_declaration = self.is_function_declared(token)
            if function_declaration:
                # todo assuming the the function matches
                if function_declaration.return_type != list_of_tokens[0]:
                    # if the first part does not match the return type,
                    # it is not a function definition
                    return -1
                next_statements = statements[line_number+1:]
                line_number += 1
                line_number += self.parse_function_definition_statement(
                    function_declaration, next_statements)
                found = True
                break
        if found is False:
            # this was not a function definition
            line_number = -1
        return line_number

    def join_lines_until_next_semicolon(self, statements):
        line_number, position = self.find_first_semicolon_in_list(statements)
        if line_number == -1:
            return line_number, None
        statement = statements[:line_number]
        statement.append(statements[line_number][:position])
        statement = ''.join(statement)
        return line_number, statement

    def join_lines_until_next_non_empty_line(self, statements):
        line_number = self.find_first_non_empty_in_list(statements)
        if line_number == -1:
            return line_number, None
        statement = statements[:line_number+1]
        statement = ''.join(statement)
        return line_number, statement

    def read_function_declaration(self, statements):
        line_number, statement = \
            self.join_lines_until_next_semicolon(statements)
        if line_number == -1:
            return line_number
        list_of_tokens = statement.split()
        if list_of_tokens[0] in self.types:
            return_type = list_of_tokens[0]
            name_start = statement.index(list_of_tokens[1])
            if '(' not in statement:
                # not a function declaration
                return -1
            if '{' in statement:
                # a '{' cannot be part of the function declaration statement
                return -1
            arg_list_start = statement.index('(')
            function_name = statement[name_start: arg_list_start]
            argument_list = \
                extractTextForEnclosedParenthesis(statement, arg_list_start)
            list_of_args = argument_list.split(',')
            function_arguments = []
            for arg in list_of_args:
                parts = arg.split()
                arg_type = parts[0]
                if arg_type == 'void':
                    depth = self.get_depth_in_tree()
                    arg_name = parts[0]
                    arg_type = None
                    function_argument = FunctionArgument(arg_type, None,
                                                         arg_name, depth)
                    function_arguments.append(function_argument)
                else:
                    res = self.extract_variable_declaration_from_string(arg)
                    if len(res) == 1:
                        depth = self.get_depth_in_tree()
                        variable_declaration = res[0]
                        variable_declaration.update_depth(depth+3)
                        function_arguments.append(variable_declaration)
            # todo check
            depth = self.get_depth_in_tree()
            function_declaration = \
                FunctionDeclaration(return_type, function_name,
                                    function_arguments, depth)
            self.current_node.add_statement(function_declaration)
            self.declared_functions.append(function_declaration)
            function_declaration.update_depth(depth)
            self.index += 1
        else:
            # not a function declaration
            line_number = -1
        return line_number

    def read_next_statement(self):
        lines = self.source_code_list[self.index:]
        processed_line_count = self.parse_line(lines)
        if processed_line_count == -1:
            self.index += 1
        else:
            # point to the line after the one(s) processed
            self.index += processed_line_count + 1

    def parse_line(self, lines):

        for line in lines:
            if '{' in line:
                break

        processed_line_count = self.read_variable(list(lines))
        if processed_line_count > -1:
            # the statement is a variable declaration
            return processed_line_count

        processed_line_count = self.read_function_declaration(list(lines))
        if processed_line_count > -1:
            # the statement is a function declaration
            return processed_line_count

        processed_line_count = self.read_function_definition(list(lines))
        if processed_line_count > -1:
            # the statement is a function definition
            return processed_line_count

        processed_line_count = self.read_compound_statement(list(lines))
        if processed_line_count > -1:
            # it is a compound statement
            return processed_line_count

        processed_line_count = self.read_function_call(list(lines))
        if processed_line_count > -1:
            # it is a function call
            return processed_line_count

        message = ''
        for line in lines:
            if line != '' and not line.isspace():
                message += 'following line not recognized:\"%s\"\n' % line
        # self.AST_error(message)
        return processed_line_count

    def to_string(self):
        string = 'FileAST: \n'
        for element in self.root_node.statement_sequence:
            string += str(element)

        return string
