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

    def is_compatible_to(self, variable_declaration):
        """
        Args:
            variable_declaration (VariableDeclaration): the variable to
            compare to
        Returns:
            bool: if the object is compatible
        """
        if isinstance(variable_declaration, FunctionArgument):
            if self.variable_type == variable_declaration.identifier:
                return True
        if self.variable_type == variable_declaration.variable_type:
            return True
        return False


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
            + self.variable_type + '\']\n'
        if self.array_size:
            string += self._depth * '  ' + '    Constant: ' + \
                      self.array_size_type + ', ' + \
                      self.array_size + '\n'
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
                string += str(expression)
        return string


class ReturnStatement(Statement):

    def __init__(self, depth, identifier):
        super(ReturnStatement, self).__init__(depth)
        self.id = identifier

    def __str__(self):
        string = self._depth * '  ' + 'Return: \n'
        string += self._depth * '  ' + '  ID: %s\n' % self.id
        return string


class Expression(AstNode):
    def __init__(self, depth, name):
        super(Expression, self).__init__(depth)
        self.name = name

    def __str__(self):
        string = self._depth * '  ' + 'ID: %s\n' % self.name
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
        """Return the type of the expression as string

        Args:
            expression (str): the expression to analyse

        Returns:
            str: the type
        """
        type_string = None
        try:
            int(expression, 0)
            type_string = 'int'
            return type_string
        except ValueError:
            # it was not a number
            pass
        ind = expression.find('\"')
        if ind > -1:
            type_string = 'string'

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
                depth = self.get_depth_in_tree()
                if '[' in identifier:
                    start_index = identifier.index('[')
                    end_index, _ = \
                        extract_closing_char(list(identifier),
                                             open_char='[',
                                             start_index=start_index,
                                             start_line=0,
                                             closing_char=']')
                    content = identifier[start_index+1:end_index]
                    array_size = None
                    array_size_type = None
                    if not initializer:
                        if content != '':
                            array_size = content
                            array_size_type = self.get_type_of_expression(
                                content)
                    else:
                        initializer_type = self.get_type_of_expression(
                            initializer)
                    name = identifier[:start_index]
                    statement = ArrayDeclaration(variable_type,
                                                 name,
                                                 initializer,
                                                 initializer_type,
                                                 array_size,
                                                 array_size_type,
                                                 depth)

                else:
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
        """
            check if the name corresponds to a known function
        Args:
            function_name (str): the identifier to check

        Returns:
            FunctionDeclaration: the declared function that corresponds to
            the function_name or None if not found
        """
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
            while len(next_statements) > 0:
                new_index = self.parse_line(next_statements)
                next_statements = next_statements[new_index+1:]
            compound_statement.update_depth(depth)
            line_number = returned_line

        return line_number

    @staticmethod
    def are_arguments_compatible(list_a, list_b):

        compatible = False
        if len(list_a) != len(list_b):
            # if the list sizes do no match, it is not compatible
            return compatible
        for i in range(len(list_a)):
            argument_a = list_a[i]
            argument_b = list_b[i]
            if not argument_a.is_compatible_to(argument_b):
                # argument_a is not compatible to argument_b
                return compatible
        # all checks passed, the lists are compatible
        compatible = True
        return compatible

    def get_variable_definition_from_id(self, name_id):

        node = self.current_node
        while node:
            for statement in node.statement_sequence:
                if isinstance(statement, VariableDeclaration):
                    if statement.name == name_id:
                        # found it
                        return statement
            node = node.parent_node
        # no match found
        return None

    def get_variables_from_ids(self, argument_string):
        arg_list = argument_string.split(',')
        variable_list = []
        for arg in arg_list:
            var_def = self.get_variable_definition_from_id(arg)
            if var_def:
                variable_list.append(var_def)
        return variable_list

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
            function_declaration = self.is_function_declared(part)
            if function_declaration:
                function_name = part
                start_index = statement.index('(')
                arguments = extractTextForEnclosedParenthesis(statement,
                                                              start_index)
                if arguments == '' or arguments.isspace():
                    depth = self.get_depth_in_tree()
                    function_call = FunctionCall(depth, function_name)
                    self.current_node.add_statement(function_call)
                else:
                    variables = self.get_variables_from_ids(arguments)
                    argument_list = function_declaration.argument_list
                    if self.are_arguments_compatible(variables, argument_list):
                        expression_list = []
                        depth = self.get_depth_in_tree() + 2
                        for variable in variables:
                            expression = Expression(depth, variable.name)
                            expression_list.append(expression)
                        function_call = FunctionCall(depth, function_name,
                                                     expression_list)
                        self.current_node.add_statement(function_call)
                    else:
                        message = 'the arguments for function %s are not ' \
                                  'compatible to the function ' \
                                  'declaration\nGot %s but expected %s' % (
                                   function_name, variables, argument_list)
                        self.ast_error(message)

        return line_number

    def check_function_argument(self, argument_a, argument_b,
                                function_declaration):
        message = None
        if hasattr(argument_a, 'type_name'):
            name_a = argument_a.type_name
        elif hasattr(argument_a, 'name'):
            name_a = argument_a.name
        if hasattr(argument_b, 'type_name'):
            name_b = argument_b.type_name
        elif hasattr(argument_b, 'name'):
            name_b = argument_b.name
        if name_a is None or name_a == 'void':
            if name_b is None or name_b == 'void':
                return message
        if name_a != name_b:
            message = 'variable name of function %s, does ' \
                      'not match the one from the ' \
                      'declaration declaration %s ' \
                      'definition %s' % \
                      (function_declaration.name,
                       name_a, name_b)

        return message

    def does_definition_and_declaration_match(self, statement,
                                              function_declaration):
        start_index = statement.index('(')
        arguments = extractTextForEnclosedParenthesis(statement,
                                                      start_index)
        args = self.extract_variable_declaration_from_string(arguments)
        if len(function_declaration.argument_list) != len(args):
            message = 'the number of arguments do not match the ' \
                      'function declaration, got %d, expected %d' % \
                      (len(args),
                       len(function_declaration.argument_list))
            self.ast_error(message)
            return -1
        for i in range(len(args)):
            argument_a = args[i]
            argument_b = function_declaration.argument_list[i]
            if argument_a.is_compatible_to(argument_b):
                message = self.check_function_argument(argument_a, argument_b,
                                                       function_declaration)
                if message:
                    self.ast_warning(message)
            else:
                if hasattr(argument_b, 'identifier'):
                    type_name = argument_b.identifier
                elif hasattr(argument_b, 'variable_type'):
                    type_name = argument_b.variable_type
                message = 'the argument type does not match the ' \
                          'expected type, Expected %s, got %s' % (
                              type_name,
                              argument_a.variable_type)
                if False:
                    # todo fix
                    self.ast_error(message)
                    return -1

        return 0

    def read_return_statement(self, code_list):
        line_number, statement = self.join_lines_until_next_semicolon(
            code_list)
        if line_number == -1:
            return line_number
        splited_statement = statement.split()
        if 'return' == splited_statement[0]:
            depth = self.get_depth_in_tree()
            if len(splited_statement) == 2:
                retval = splited_statement[1]
                if self.get_variable_definition_from_id(retval):
                    return_statement = ReturnStatement(depth, retval)
                    self.current_node.add_statement(return_statement)
                else:
                    # probably is a constant expression
                    pass
        return line_number

    def read_function_definition(self, statements):
        found = False

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
                if function_declaration.return_type != list_of_tokens[0]:
                    # if the first part does not match the return type,
                    # it is not a function definition
                    return -1
                result = self.\
                    does_definition_and_declaration_match(statement,
                                                          function_declaration)
                if result == -1:
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

        processed_line_count = self.read_return_statement(list(lines))
        if processed_line_count > -1:
            # it is a function call
            return processed_line_count

        message = ''
        for line in lines:
            if line != '' and not line.isspace():
                message += 'following line not recognized:\"%s\"\n' % line
        return processed_line_count

    def to_string(self):
        string = 'FileAST: \n'
        for element in self.root_node.statement_sequence:
            string += str(element)

        return string
