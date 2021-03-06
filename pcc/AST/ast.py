import copy
import re

import pcc
import pcc.utils.warning
from pcc import utils
from pcc.AST.arithmetic_operators.addition import Addition
from pcc.AST.array_declaration import ArrayDeclaration
from pcc.AST.variables.assignment import Assignment
from pcc.AST.ast_node import AstNode
from pcc.AST.bitwise_operators.bitwise_and import BitwiseAnd
from pcc.AST.bitwise_operators.bitwise_not import BitwiseNot
from pcc.AST.bitwise_operators.bitwise_or import BitwiseOr
from pcc.AST.bitwise_operators.bitwise_xor import BitwiseXor
from pcc.AST.comparisons.compare_equal import CompareEqual
from pcc.AST.comparisons.compare_less import CompareLess
from pcc.AST.comparisons.compare_less_or_equal import CompareLessOrEqual
from pcc.AST.comparisons.compare_more import CompareMore
from pcc.AST.comparisons.compare_more_or_equal import CompareMoreOrEqual
from pcc.AST.comparisons.compare_not_equal import CompareNotEqual
from pcc.AST.compound_statement import CompoundStatement
from pcc.AST.constant_expression import ConstantExpression
from pcc.AST.arithmetic_operators.division import Division
from pcc.AST.functions.function_argument import FunctionArgument
from pcc.AST.functions.function_call import FunctionCall
from pcc.AST.functions.function_declaration import FunctionDeclaration
from pcc.AST.functions.function_definition import FunctionDefinition
from pcc.AST.control_statements.if_statement import IfStatement
from pcc.AST.logical_operators.logical_and import LogicalAnd
from pcc.AST.logical_operators.logical_not import LogicalNot
from pcc.AST.logical_operators.logical_or import LogicalOr
from pcc.AST.arithmetic_operators.multiplication import Multiplication
from pcc.AST.return_statement import ReturnStatement
from pcc.AST.arithmetic_operators.subtraction import Subtraction
from pcc.AST.variables.variable_declaration import VariableDeclaration
from pcc.AST.variables.variable_reference import VariableReference
from pcc.AST.control_statements.while_statement import WhileStatement
from pcc.utils.stringListParsing import extract_closing_char
from pcc.utils.stringParsing import extract_text_for_enclosed_parenthesis


class VariableType:
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def __str__(self):
        string = f'Variable type; name: {self.name}, size:{self.size}'
        return string


class Ast:
    c_types = [VariableType('int', 4),
               VariableType('char', 1),
               VariableType('float', 4),
               VariableType('double', 8),
               VariableType('void', 0)]

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

    def get_type_from_name(self, type_name):
        """Get the type from the type name.

        Args:
            type_name (str): The name of the type

        Returns:
            VariableType: the type for the variable name
        """
        for known_type in self.types:
            if known_type.name == type_name:
                return known_type
        return None

    def ast_warning(self, message):
        pcc.utils.warning.warning(self.filename,
                                  self.index, message)

    def ast_error(self, message):
        pcc.utils.warning.warning(self.filename,
                                  self.index, message)

    def get_depth_in_tree(self):
        depth = 1
        node = self.current_node
        self.tree_string = self.__str__()
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
        if not expression:
            # no valid expression, so None type
            return type_string
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

        ind = expression.find('.')
        if ind > -1:
            type_string = 'double'
            return type_string

        ind = expression.find('\'')
        if ind > -1:
            type_string = 'char'
            return type_string

        return type_string

    def _extract_arithmetic_expression(self, right_hand_value, depth):
        """Extract the arithmetic expression from string

        Args:
            right_hand_value (str): the expression to parse
            depth (int): the depth in the tree

        Returns:
            Expression: the expression if parsed else None
        """
        # the initializer of a big double might use scientific notation
        # e.g. 1e+3
        # must match optional number and optional fraction with e or E
        # and +- an
        # exponent
        exp_regex = re.compile(r"((-)?\d+(\.\d+)?)[Ee]([+\-])(\d+)")
        regex_number_result = exp_regex.match(right_hand_value)

        res_addition = re.match(r"(\S+)\+(\S+)", right_hand_value)
        res_subtraction = re.match(r"(\S+)-(\S+)", right_hand_value)

        res_division = re.match(r"(\S+)/(\S+)", right_hand_value)
        res_multiplication = re.match(r"(\S+)\*(\S+)", right_hand_value)

        if res_addition and not regex_number_result:

            operand_1_str = res_addition.group(1)
            operand_1 = self.get_right_hand_value(operand_1_str, depth)

            operand_2_str = res_addition.group(2)
            operand_2 = self.get_right_hand_value(operand_2_str, depth)

            expression = Addition(depth, operand_1, operand_2)
        elif res_subtraction and not regex_number_result:

            operand_1_str = res_subtraction.group(1)
            operand_1 = self.get_right_hand_value(operand_1_str, depth)

            operand_2_str = res_subtraction.group(2)
            operand_2 = self.get_right_hand_value(operand_2_str, depth)

            expression = Subtraction(depth, operand_1, operand_2)

        elif res_division:
            operand_1_str = res_division.group(1)
            operand_1 = self.get_right_hand_value(operand_1_str, depth)

            operand_2_str = res_division.group(2)
            operand_2 = self.get_right_hand_value(operand_2_str, depth)

            expression = Division(depth, operand_1, operand_2)
        elif res_multiplication:
            operand_1_str = res_multiplication.group(1)
            operand_1 = self.get_right_hand_value(operand_1_str, depth)

            operand_2_str = res_multiplication.group(2)
            operand_2 = self.get_right_hand_value(operand_2_str, depth)

            expression = Multiplication(depth, operand_1, operand_2)
        else:
            expression = None

        return expression

    def _extract_bitwise_expression(self, right_hand_value, depth):
        """Extract the bitwise expression from string

        Args:
            right_hand_value (str): the expression to parse
            depth (int): the depth in the tree

        Returns:
            Expression: the expression if parsed else None
        """
        res_bitwise_and = re.match(r"(\S+)&(\S+)", right_hand_value)
        res_bitwise_or = re.match(r"(\S+)\|(\S+)", right_hand_value)
        res_bitwise_xor = re.match(r"(\S+)\^(\S+)", right_hand_value)
        res_bitwise_not = re.match(r"~(\S+)", right_hand_value)
        if res_bitwise_and:
            operand_1_str = res_bitwise_and.group(1)
            operand_1 = self.get_right_hand_value(operand_1_str, depth)

            operand_2_str = res_bitwise_and.group(2)
            operand_2 = self.get_right_hand_value(operand_2_str, depth)

            expression = BitwiseAnd(depth, operand_1, operand_2)
        elif res_bitwise_or:
            operand_1_str = res_bitwise_or.group(1)
            operand_1 = self.get_right_hand_value(operand_1_str, depth)

            operand_2_str = res_bitwise_or.group(2)
            operand_2 = self.get_right_hand_value(operand_2_str, depth)

            expression = BitwiseOr(depth, operand_1, operand_2)
        elif res_bitwise_xor:
            operand_1_str = res_bitwise_xor.group(1)
            operand_1 = self.get_right_hand_value(operand_1_str, depth)

            operand_2_str = res_bitwise_xor.group(2)
            operand_2 = self.get_right_hand_value(operand_2_str, depth)

            expression = BitwiseXor(depth, operand_1, operand_2)
        elif res_bitwise_not:
            operand_1_str = res_bitwise_not.group(1)
            operand_1 = self.get_right_hand_value(operand_1_str, depth)

            expression = BitwiseNot(depth, operand_1)
        else:
            expression = None

        return expression

    def _extract_logical_expression(self, right_hand_value, depth):
        """Extract the logical expression from string

        Args:
            right_hand_value (str): the expression to parse
            depth (int): the depth in the tree

        Returns:
            Expression: the expression if parsed else None
        """
        res_logical_and = re.match(r"(\S+)&&(\S+)", right_hand_value)
        res_logical_or = re.match(r"(\S+)\|\|(\S+)", right_hand_value)
        res_logical_not = re.match(r"!(\S+)", right_hand_value)

        if res_logical_and:
            operand_1_str = res_logical_and.group(1)
            operand_1 = self.get_right_hand_value(operand_1_str, depth)

            operand_2_str = res_logical_and.group(2)
            operand_2 = self.get_right_hand_value(operand_2_str, depth)

            expression = LogicalAnd(depth, operand_1, operand_2)
        elif res_logical_or:
            operand_1_str = res_logical_or.group(1)
            operand_1 = self.get_right_hand_value(operand_1_str, depth)

            operand_2_str = res_logical_or.group(2)
            operand_2 = self.get_right_hand_value(operand_2_str, depth)

            expression = LogicalOr(depth, operand_1, operand_2)
        elif res_logical_not:
            operand_1_str = res_logical_not.group(1)
            operand_1 = self.get_right_hand_value(operand_1_str, depth)

            expression = LogicalNot(depth, operand_1)
        else:
            expression = None

        return expression

    def _extract_compare_expression(self, right_hand_value, depth):
        """Extract the compare expression from string.

        Args:
            right_hand_value (str): the expression to parse
            depth (int): the depth in the tree

        Returns:
            Expression: the expression if parsed else None
        """
        res_compare_equal = re.match(r"([^=]+)==([^=]+)", right_hand_value)
        res_compare_not_equal = re.match(r"([^=!]+)!=([^=!]+)",
                                         right_hand_value)

        res_compare_less = re.match(r"([^<]+)<([^<]+)", right_hand_value)
        res_compare_more = re.match(r"([^>]+)>([^>]+)", right_hand_value)

        res_compare_less_or_equal = re.match(r"([^<=]+)<=([^<=]+)",
                                             right_hand_value)
        res_compare_more_or_equal = re.match(r"([^>=]+)>=([^>=]+)",
                                             right_hand_value)

        if res_compare_equal:
            operand_1_str = res_compare_equal.group(1)
            operand_1 = self.get_right_hand_value(operand_1_str, depth)

            operand_2_str = res_compare_equal.group(2)
            operand_2 = self.get_right_hand_value(operand_2_str, depth)

            expression = CompareEqual(depth, operand_1, operand_2)
        elif res_compare_not_equal:
            operand_1_str = res_compare_not_equal.group(1)
            operand_1 = self.get_right_hand_value(operand_1_str, depth)

            operand_2_str = res_compare_not_equal.group(2)
            operand_2 = self.get_right_hand_value(operand_2_str, depth)

            expression = CompareNotEqual(depth, operand_1, operand_2)

        elif res_compare_more_or_equal:
            operand_1_str = res_compare_more_or_equal.group(1)
            operand_1 = self.get_right_hand_value(operand_1_str, depth)

            operand_2_str = res_compare_more_or_equal.group(2)
            operand_2 = self.get_right_hand_value(operand_2_str, depth)

            expression = CompareMoreOrEqual(depth, operand_1, operand_2)
        elif res_compare_less_or_equal:
            operand_1_str = res_compare_less_or_equal.group(1)
            operand_1 = self.get_right_hand_value(operand_1_str, depth)

            operand_2_str = res_compare_less_or_equal.group(2)
            operand_2 = self.get_right_hand_value(operand_2_str, depth)

            expression = CompareLessOrEqual(depth, operand_1, operand_2)
        elif res_compare_less:
            operand_1_str = res_compare_less.group(1)
            operand_1 = self.get_right_hand_value(operand_1_str, depth)

            operand_2_str = res_compare_less.group(2)
            operand_2 = self.get_right_hand_value(operand_2_str, depth)

            expression = CompareLess(depth, operand_1, operand_2)
        elif res_compare_more:
            operand_1_str = res_compare_more.group(1)
            operand_1 = self.get_right_hand_value(operand_1_str, depth)

            operand_2_str = res_compare_more.group(2)
            operand_2 = self.get_right_hand_value(operand_2_str, depth)

            expression = CompareMore(depth, operand_1, operand_2)
        else:
            expression = None

        return expression

    def get_right_hand_value(self, right_hand_value, depth):
        """Extract the right hand value out the string

        Args:
            right_hand_value (str): the string representation
            depth (int): depth in the tree

        Returns:
            Expression: the expression if correctly parsed else None
        """
        if not right_hand_value:
            expression = None
        else:
            initializer_type = self.get_type_of_expression(right_hand_value)

            arithmetic_exp = self._extract_arithmetic_expression(
                right_hand_value, depth)
            logical_exp = self._extract_logical_expression(right_hand_value,
                                                           depth)
            bitwise_exp = self._extract_bitwise_expression(right_hand_value,
                                                           depth)
            compare_exp = self._extract_compare_expression(right_hand_value,
                                                           depth)

            if arithmetic_exp:
                expression = arithmetic_exp
            elif logical_exp:
                expression = logical_exp
            elif self.get_variable_definition_from_id(right_hand_value):
                expression = VariableReference(depth, right_hand_value.strip())
                expression.parent_node = self.current_node
            elif bitwise_exp:
                expression = bitwise_exp
            elif compare_exp:
                expression = compare_exp
            else:
                function_call = self.parse_function_call(right_hand_value)
                if function_call:
                    expression = function_call
                else:
                    expression = ConstantExpression(initializer_type,
                                                    right_hand_value.strip(),
                                                    depth)

        return expression

    def extract_variable_declaration_from_string(self, statement):
        list_of_tokens = statement.split()
        result_list = []
        is_extern = False
        if list_of_tokens[0] == 'extern':
            list_of_tokens.pop(0)
            # remove the extern keyword from the statement and continue
            statement = ' '.join(list_of_tokens)
            is_extern = True
        variable_type = self.get_type_from_name(list_of_tokens[0])
        if variable_type:
            declarations = statement.replace(variable_type.name + ' ', '')
            list_of_declarations = declarations.split(',')
            for declaration in list_of_declarations:
                tmp_decl = declaration.split()
                if len(tmp_decl) > 1:
                    variable_type_tmp = self.get_type_from_name(tmp_decl[0])
                    if variable_type_tmp and variable_type_tmp.name != 'void':
                        variable_type = variable_type_tmp
                        declaration = ''.join(tmp_decl[1:])
                if '=' in declaration:
                    parts = declaration.split('=')
                    identifier = parts[0]
                    # comparisons might still have equals signs inside, so
                    # add them back to the initializer
                    initializer = '='.join(parts[1:])
                    # remove all whitespace chars from initializer
                    initializer = ''.join(initializer.split())
                else:
                    identifier = declaration
                    initializer = None
                # remove all whitespace chars from identifier
                identifier = ''.join(identifier.split())
                if '(' in identifier:
                    # there cannot be a parenthesis in the variable name,
                    # this is probably a function
                    return []
                depth = self.get_depth_in_tree()
                if '[' in identifier:
                    statement = self.parse_array_declaration(depth, identifier,
                                                             initializer,
                                                             variable_type)
                else:
                    initializer_exp = self.get_right_hand_value(initializer,
                                                                depth)
                    statement = VariableDeclaration(variable_type,
                                                    identifier,
                                                    initializer_exp,
                                                    depth,
                                                    is_extern)
                result_list.append(statement)
        return result_list

    def parse_array_declaration(self, depth, identifier, initializer,
                                variable_type):
        start_index = identifier.index('[')
        end_index, _ = \
            extract_closing_char(list(identifier),
                                 open_char='[',
                                 start_index=start_index,
                                 start_line=0,
                                 closing_char=']')
        content = identifier[start_index + 1:end_index]
        array_size = None
        array_size_type = None
        if content != '':
            array_size = content
            array_size_type = self.get_type_of_expression(
                content)
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
        return statement

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
        """Check if the name corresponds to a known function.

        Args:
            function_name (str): the identifier to check

        Returns:
            pcc.AST.function_declaration.FunctionDeclaration: the
                declared function that corresponds to the function_name or None
                if not found
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
        decl.update_depth(depth + 1)
        self.current_node.add_statement(decl)

        line_number = self.parse_line(statements)
        if line_number == -1:
            message = 'could not find the definition of function %s' % \
                      function_declaration.name
            self.ast_error(message)
        else:
            # the function definition is complete go back up to its parent
            self.current_node = function_definition.parent_node
        return line_number

    def read_compound_statement(self, code_list):
        line_number = -1
        list_to_process = code_list
        open_char = '{'
        start_line = 0
        start_index = 0
        closing_char = '}'

        text = ''.join(code_list).lstrip()
        if len(text) > 0 and text[0] != open_char:
            return line_number

        returned_line, returned_index = \
            extract_closing_char(list_to_process, open_char, start_line,
                                 start_index, closing_char)
        if returned_line != -1 and returned_index != -1:

            depth = self.get_depth_in_tree()
            compound_statement = CompoundStatement(depth)
            self.current_node.add_statement(compound_statement)
            self.current_node = compound_statement
            next_statements = code_list[start_line + 1:returned_line]
            while len(next_statements) > 0:
                new_index = self.parse_line(next_statements)
                next_statements = next_statements[new_index + 1:]
            compound_statement.update_depth(depth)
            line_number = returned_line
            self.current_node = compound_statement.parent_node

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
                    if statement.name == name_id.strip():
                        # found it
                        return statement
                elif isinstance(statement, FunctionDeclaration):
                    for argument in statement.argument_list:
                        if isinstance(argument, FunctionArgument) and \
                                argument.identifier == name_id.strip():
                            return argument
                        elif isinstance(argument, VariableDeclaration) and \
                                argument.name == name_id.strip():
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

    def parse_function_call(self, expression):
        function_call = None
        part = expression.split('(')[0].lstrip().rstrip()
        function_declaration = self.is_function_declared(part)
        if function_declaration:
            function_name = part
            start_index = expression.index('(')
            arguments = extract_text_for_enclosed_parenthesis(expression,
                                                              start_index)
            if arguments == '' or arguments.isspace():
                depth = self.get_depth_in_tree()
                function_call = FunctionCall(depth, function_name)
            else:
                variables = self.get_variables_from_ids(arguments)
                argument_list = function_declaration.argument_list
                if self.are_arguments_compatible(variables, argument_list):
                    expression_list = []
                    depth = self.get_depth_in_tree() + 1
                    for variable in variables:
                        expression = VariableReference(depth,
                                                       variable.name)
                        expression_list.append(expression)
                    function_call = FunctionCall(depth, function_name,
                                                 expression_list)
        return function_call

    def read_function_call(self, code_list):
        line_number, statement = self.join_lines_until_next_semicolon(
            code_list)
        if line_number == -1:
            return line_number
        if '(' not in statement:
            # a function call always has an opening and closing bracket
            return -1

        function_call = self.parse_function_call(statement)
        if function_call:
            self.current_node.add_statement(function_call)
        else:
            line_number = -1

        return line_number

    @staticmethod
    def check_function_argument(argument_a, argument_b,
                                function_declaration):
        message = None
        if hasattr(argument_a, 'type_name'):
            name_a = argument_a.type_name
        elif hasattr(argument_a, 'name'):
            name_a = argument_a.name
        else:
            name_a = None
        if hasattr(argument_b, 'type_name'):
            name_b = argument_b.type_name
        elif hasattr(argument_b, 'name'):
            name_b = argument_b.name
        else:
            name_b = None
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
        arguments = extract_text_for_enclosed_parenthesis(statement,
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
                else:
                    type_name = None
                message = 'the argument type does not match the ' \
                          'expected type, Expected %s, got %s' % (
                              type_name,
                              argument_a.variable_type)
                self.ast_error(message)
                return -1

        return 0

    def read_return_statement(self, code_list):
        line_number, statement = self.join_lines_until_next_semicolon(
            code_list)
        if line_number == -1:
            return line_number
        splitted_statement = statement.split()
        if 'return' == splitted_statement[0]:
            depth = self.get_depth_in_tree()
            if len(splitted_statement) == 2:
                retval = splitted_statement[1]
                if self.get_variable_definition_from_id(retval):
                    expression = VariableReference(depth, retval)
                    return_statement = ReturnStatement(depth, expression)
                    expression.parent_node = self.current_node
                    self.current_node.add_statement(return_statement)
                else:
                    # probably is a constant expression
                    func_def = self.current_node.get_function_definition_node()
                    if func_def:
                        expression_type = self.get_type_of_expression(retval)
                        expression_value = retval
                        depth = self.get_depth_in_tree()
                        expression = ConstantExpression(expression_type,
                                                        expression_value,
                                                        depth)
                        return_statement = ReturnStatement(depth, expression)
                        self.current_node.add_statement(return_statement)
                    else:
                        message = 'Could not find the function definition ' \
                                  'of the return statement'
                        self.ast_error(message)
                        line_number = -1
                        return line_number

            else:
                expression = None
                return_statement = ReturnStatement(depth, expression)
                self.current_node.add_statement(return_statement)
        else:
            line_number = -1
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
                if function_declaration.return_type.name != list_of_tokens[0]:
                    # if the first part does not match the return type,
                    # it is not a function definition
                    return -1
                result = self. \
                    does_definition_and_declaration_match(statement,
                                                          function_declaration)
                if result == -1:
                    return -1
                next_statements = statements[line_number + 1:]
                line_number += 1
                line_number += self.parse_function_definition_statement(
                    function_declaration, next_statements)
                found = True
                break
        if found is False:
            # this was not a function definition
            line_number = -1
        return line_number

    def read_assignment(self, statements):
        found = False

        line_number, statement = self.join_lines_until_next_non_empty_line(
            statements)
        if line_number == -1:
            return line_number
        list_of_tokens = statement.split()

        var_to_update = list_of_tokens[0]
        if len(list_of_tokens) < 2:
            return -1
        initializer = ' '.join(list_of_tokens[2:])
        if list_of_tokens[1] == '=':
            found = True
        if '=' in var_to_update:
            tmp = var_to_update.split('=')
            var_to_update = tmp[0]
            initializer = ' '.join(tmp[1:]) + initializer
            found = True

        if found:
            depth = self.get_depth_in_tree()
            # remove all whitespace chars from initializer
            initializer = ''.join(initializer.split())
            initializer = initializer.split(';')[0]

            expression = self.get_right_hand_value(initializer, depth)
            assignment = Assignment(depth, var_to_update, expression)
            self.current_node.add_statement(assignment)

        if found is False:
            # this was not an assignment
            line_number = -1
        return line_number

    def read_if_statement(self, statements):

        line_number, statement = self.join_lines_until_next_non_empty_line(
            statements)
        if line_number == -1:
            return line_number

        if statement.strip().startswith('if'):
            depth = self.get_depth_in_tree()
            start_index = statement.find('if') + len('if')
            end_line, end_pos = utils.stringListParsing.extract_closing_char(
                list_to_process=statements,
                open_char='(',
                start_line=0,
                start_index=start_index,
                closing_char=')')
            if end_line == 0:
                condition_str = statement[start_index+1:end_pos]
            else:
                condition_str = statement[start_index+1:]
                condition_str += statements[1:end_line]
                condition_str += statements[end_line][:end_pos]
            # the condition is one deeper than the if condition
            condition = None
            if_branch = None
            else_branch = None
            if_statement = IfStatement(depth, condition,
                                       if_branch, else_branch)
            self.current_node.add_statement(if_statement)
            self.current_node = if_statement
            condition = self.get_right_hand_value(condition_str, depth)
            if_statement.condition = condition
            # found a correct if line
            line_number += 1 + end_line
            next_statements = statements[line_number:]
            processed_lines = self.parse_line(next_statements)
            if processed_lines == -1:
                self.ast_error("could not process the if branch %s" %
                               ''.join(next_statements))
                return -1
            if len(if_statement.statement_sequence) != 1:
                self.ast_error("could not recognise the statements %s" %
                               ''.join(next_statements))
                return -1
            # move the if statement inside the object instead of the list
            if_statement.if_statement = if_statement.statement_sequence[0]
            if_statement.statement_sequence.pop()

            next_statements = next_statements[processed_lines + 1:]
            # update the number of processed lines
            line_number += processed_lines

            # check if there is an else branch
            line_number_else, statement = \
                self.join_lines_until_next_non_empty_line(
                    next_statements)
            match_obj = re.match(r"\s+else(\S?)", statement)
            if match_obj:
                else_str = match_obj.group(1)
                next_statements = next_statements[line_number_else + 1:]
                if else_str:
                    next_statements.insert(else_str, 0)
                processed_lines = self.parse_line(next_statements)
                if processed_lines == -1:
                    self.ast_error("could not process the else branch %s" %
                                   ''.join(next_statements))
                    return -1
                if len(if_statement.statement_sequence) != 1:
                    self.ast_error("could not recognise the statements %s" %
                                   ''.join(next_statements))
                    return -1
                # move the else statement inside the object instead of the list
                if_statement.else_statement = \
                    if_statement.statement_sequence[0]
                if_statement.statement_sequence.pop()

                line_number += (line_number_else + 1)
                line_number += (processed_lines + 1)

            # set the current node back tot he parent of the if statement
            self.current_node = if_statement.parent_node

        else:
            # this was not an if statement
            line_number = -1
        return line_number

    def read_while_statement(self, statements):

        line_number, statement = self.join_lines_until_next_non_empty_line(
            statements)
        if line_number == -1:
            return line_number

        while_stat = re.match(r"\s+while\((\S+)\)", statement)

        if while_stat:
            depth = self.get_depth_in_tree()
            condition_str = while_stat.group(1)
            # the condition is one deeper than the if condition
            condition = self.get_right_hand_value(condition_str, depth)
            body = None
            while_statement = WhileStatement(depth, condition, body)
            self.current_node.add_statement(while_statement)
            self.current_node = while_statement
            # found a correct condition line
            line_number += 1
            next_statements = statements[line_number:]
            processed_lines = self.parse_line(next_statements)
            if processed_lines == -1:
                self.ast_error("could not process the body of the while %s" %
                               ''.join(next_statements))
                return -1
            if len(while_statement.statement_sequence) != 1:
                self.ast_error("could not recognise the statements %s" %
                               ''.join(next_statements))
                return -1
            # move the body statement inside the object instead of the list
            while_statement.body_statement = \
                while_statement.statement_sequence[0]
            while_statement.statement_sequence.pop()

            # update the number of processed lines
            line_number += processed_lines

            # set the current node back tot he parent of the while statement
            self.current_node = while_statement.parent_node

        else:
            # this was not a while statement
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
        statement = statements[:line_number + 1]
        statement = ''.join(statement)
        return line_number, statement

    def read_function_declaration(self, statements):
        line_number, statement = \
            self.join_lines_until_next_semicolon(statements)
        if line_number == -1:
            return line_number
        list_of_tokens = statement.split()
        variable_type = self.get_type_from_name(list_of_tokens[0])
        if variable_type:
            return_type = variable_type
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
                extract_text_for_enclosed_parenthesis(statement,
                                                      arg_list_start)
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
                        variable_declaration.update_depth(depth + 3)
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
        """Parse the lines of code.

        Args:
            lines ([str]): the lines of code

        Returns:
            int: the number of processed lines or -1 in case of error
        """
        processed_line_count = -1

        # if there is nothing left, consider the line parsed
        if len(lines) == 1 and not lines[0]:
            return 1

        list_of_parsing_methods = [
            self.read_variable,
            self.read_function_declaration,
            self.read_function_definition,
            self.read_compound_statement,
            self.read_function_call,
            self.read_return_statement,
            self.read_assignment,
            self.read_if_statement,
            self.read_while_statement,
        ]
        for method in list_of_parsing_methods:
            processed_line_count = method(list(lines))
            if processed_line_count > -1:
                # the lines have been parsed correctly
                return processed_line_count

        message = ''
        for line in lines:
            if line != '' and not line.isspace():
                message += 'following line not recognized:\"%s\"\n' % line
        return processed_line_count

    def __str__(self):
        string = 'FileAST: \n'
        for element in self.root_node.statement_sequence:
            string += str(element)

        return string
