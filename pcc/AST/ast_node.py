
import copy
import enum
import struct

from pcc.compiler.assembler import ProcessorRegister


def push_variable_on_stack(assembler, stack_offset,
                           stack_var, value, value_array):
    """Push a value on a specified location on stack

    Args:
        assembler (Assembler): the assembler to use
        stack_offset (int): the offset relative to the current stack pointer
        stack_var (StackVariable): the stack variable
        value (bytearray): the byte array to append the machine code to
        value_array (bytearray): the bytearray to push to stack

    Returns:
        bytearray: the array with the added machine code
        int: the stackoffset
    """

    number_of_words = int((len(value_array) - 1) / 4) + 1
    for i in range(number_of_words):
        part_of_array = value_array[i * 4:(i + 1) * 4]
        stack_offset -= 4
        value += assembler.push_value_to_stack(part_of_array, stack_offset)

    # if multiple words are used, move the offset a word further
    if number_of_words > 1:
        stack_offset -= 4
    return value, stack_offset


class CompiledObjectType(enum.Enum):
    data = 1,
    code = 2,


class CompiledObject:

    def __init__(self, name, size, value, objectType):
        """Create an compiled object.

        Args:
            name (str): the name of the object
            size (int): the size of the object
            value (bytearray): the content of the object
            objectType (CompiledObjectType): the type of object

        """
        self.name = name
        self.size = size
        self.value = value
        self.type = objectType


class StackVariable:
    def __init__(self, name, size, initializer_byte_array, type_name):
        self.name = name
        self.size = size
        self.initializer_byte_array = initializer_byte_array
        self.stack_offset = 0
        self.stack_start = 0
        self.type_name = type_name


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

    def get_function_definition_node(self):
        """Get the function definition if found.

        Returns (FunctionDefinition): the definition if found else None

        """
        return None

    def add_stack_variable(self, current_list):
        """Add all stack variable to the list

        Args:
            current_list(list[StackVariable]): the current list
        """
        pass

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

    def get_function_definition_node(self):
        """Get the function definition if found.

        Returns (FunctionDefinition): the definition if found else None

        """
        return self.parent_node.get_function_definition_node()


class VariableDeclaration(Statement):

    def __init__(self, variable_type, name, initializer, depth):
        """Create a variable declaration.

        Args:
            variable_type (str): the type
            name (str): the name of the variable
            initializer (Expression): the expression to initialize
            depth (int): the depth in the tree
        """
        super(VariableDeclaration, self).__init__(depth)
        self.variable_type = variable_type
        self.name = name
        self.initializer = initializer
        self.stack_var = None

    def __str__(self):
        string = self._depth * '  ' + 'Decl: ' + self.name + ', [], [], []\n'
        string += self._depth * '  ' + '  TypeDecl: ' + self.name + ', []\n'
        string += self._depth * '  ' + '    IdentifierType: [\'' \
            + self.variable_type.name + '\']\n'
        if self.initializer:
            string += self._depth * '  ' + str(self.initializer) + '\n'
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
            else:
                return False
        if self.variable_type == variable_declaration.variable_type:
            return True
        return False

    def compile(self, assembler):
        """Compile this statement

        Args:
            assembler (Assembler)
        Returns:
            CompiledObject: the compiled version of this statement
        """
        size = self.variable_type.size
        value = bytearray()
        compiled_object = None
        if self.parent_node.parent_node:
            if self.initializer:
                stack_variable = self.stack_var
                stack_offset = stack_variable.stack_offset
                if stack_variable.type_name == 'double':
                    register = ProcessorRegister.double_scalar_0
                elif stack_variable.type_name == 'float':
                    register = ProcessorRegister.single_scalar_0
                else:
                    register = ProcessorRegister.accumulator

                value += self.initializer.load_result_to_reg(register,
                                                             assembler)

                value += assembler.copy_reg_to_stack(stack_offset, register)
                compiled_object = CompiledObject(self.name, size, value,
                                                 CompiledObjectType.data)
        else:
            if self.initializer:
                value = self.initializer_to_bytearray(size)
            compiled_object = CompiledObject(self.name, size, value,
                                             CompiledObjectType.data)

        return compiled_object

    def initializer_to_bytearray(self, size):
        """Fill in the value of the initializer.

        Args:
            size (int): the size of the initializer

        Returns:
            bytearray: the byte array representation of the initializer
        """
        value = bytearray()
        initializer = self.initializer.exp_value
        if '.' in initializer:
            initializer = float(initializer)
            if self.variable_type.name == 'double':
                value = bytearray(struct.pack("d", initializer))
            else:
                value = bytearray(struct.pack("f", initializer))
        else:
            initializer = int(initializer, base=0)
            for i in range(size):
                tmp = initializer >> (i * 8)
                tmp &= 0xff
                value.append(tmp)
        return value

    def add_stack_variable(self, current_list):
        """Add all stack variable to the list

        Args:
            current_list(list[StackVariable]): the current list
        """
        # not for global variables (global variables have the root node as
        # parent who does not have a parent)
        if self.parent_node.parent_node:
            if self.initializer:
                size = self.variable_type.size
                initializer = bytearray([0x0] * size)
            else:
                initializer = 0
            stack_var = StackVariable(self.name, self.variable_type.size,
                                      initializer, self.variable_type.name)
            self.stack_var = stack_var
            current_list.append(stack_var)


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
            + self.return_type.name + '\']\n'
        return string

    def __deepcopy__(self, memodict={}):
        return_type = self.return_type
        name = self.name
        argument_list = copy.deepcopy(self.argument_list)
        depth = self._depth
        new_copy = type(self)(return_type, name, argument_list, depth)
        return new_copy

    def add_stack_variable(self, current_list):
        """Add all stack variable to the list

        Args:
            current_list(list[StackVariable]): the current list
        """
        if len(self.statement_sequence) > 1:
            self.statement_sequence[1].add_stack_variable(current_list)

    def update_depth(self, depth):
        super(FunctionDeclaration, self).update_depth(depth)
        for argument in self.argument_list:
            argument.update_depth(depth+3)

    def compile(self, assembler):
        """Compile this statement

        Args:
            assembler (Assembler)
        Returns:
            CompiledObject: the compiled version of this statement
        """
        return None

    def get_stack_variable(self, variable_name):
        """Get the stack variable by name.

        Args:
            variable_name (str): the name of the variable

        Returns:
            StackVariable: the stack variable if found, else None
        """
        return self.parent_node.get_stack_variable(variable_name)


class FunctionDefinition(Statement):

    def __init__(self, depth):
        super(FunctionDefinition, self).__init__(depth)
        self.stack_variable_list = []

    def __str__(self):
        string = self._depth * '  ' + 'FuncDef: \n'
        for arg in self.statement_sequence:
            string += str(arg)
        return string

    def get_function_definition_node(self):
        """Get the  function  definition if found.

        Returns(FunctionDefinition): self

        """
        return self

    def add_stack_variable(self, current_list):
        """Add all stack variable to the list

        Args:
            current_list(list[StackVariable]): the current list
        """
        self.statement_sequence[1].add_stack_variable(current_list)

    def get_return_type(self):
        """Get the return type.

        Returns:
            str: the return type
        """
        return self.statement_sequence[0].return_type.name

    def get_stack_variable(self, variable_name):
        """Get the stack variable by name.

        Args:
            variable_name (str): the name of the variable

        Returns:
            StackVariable: the stack variable if found, else None
        """
        stack_variable = None

        for var in self.stack_variable_list:
            if var.name == variable_name:
                stack_variable = var

        return stack_variable

    def compile(self, assembler):
        """Compile this statement.

        Args:
            assembler (Assembler)
        Returns:
            CompiledObject: the compiled version of this statement
        """
        value = bytearray()

        # save the frame pointer on stack
        ret = assembler.push_to_stack(ProcessorRegister.base_pointer)
        value.extend(ret)

        # set the stack pointer as the new base pointer
        ret = assembler.copy_from_reg_to_reg(ProcessorRegister.base_pointer,
                                             ProcessorRegister.frame_pointer)
        value.extend(ret)

        current_list = []
        self.add_stack_variable(current_list)
        # first the frame pointer has been saved to stack
        stack_offset = 0
        for stack_var in current_list:
            stack_var.stack_start = stack_offset
            value_array = stack_var.initializer_byte_array
            value, stack_offset = push_variable_on_stack(assembler,
                                                         stack_offset,
                                                         stack_var,
                                                         value,
                                                         value_array)
            stack_var.stack_offset = stack_offset

        self.stack_variable_list = current_list
        # add a nop
        ret = assembler.nop()
        value.extend(ret)

        for statement in self.statement_sequence:
            result = statement.compile(assembler)
            if result:
                value += result.value

        size = len(value)
        compiled_object = CompiledObject(self.statement_sequence[0].name, size,
                                         value, CompiledObjectType.code)

        return compiled_object


class CompoundStatement(Statement):

    def __init__(self, depth):
        super(CompoundStatement, self).__init__(depth)

    def __str__(self):
        string = self._depth * '  ' + 'Compound: \n'
        for arg in self.statement_sequence:
            string += str(arg)
        return string

    def get_return_type(self):
        """Get the return type.

        Returns:
            str: the return type
        """
        return self.parent_node.get_return_type()

    def compile(self, assembler):
        """Compile this statement

        Args:
            assembler (Assembler)
        Returns:
            CompiledObject: the compiled version of this statement
        """
        value = bytearray()
        for statement in self.statement_sequence:
            result = statement.compile(assembler)
            if result:
                value += result.value

        size = len(value)
        compiled_object = CompiledObject('compoundStatement', size,
                                         value, CompiledObjectType.code)
        return compiled_object

    def add_stack_variable(self, current_list):
        """Add all stack variable to the list

        Args:
            current_list(list[StackVariable]): the current list
        """
        if len(self.statement_sequence) > 0:
            self.statement_sequence[0].add_stack_variable(current_list)

    def get_stack_variable(self, variable_name):
        """Get the stack variable by name.

        Args:
            variable_name (str): the name of the variable

        Returns:
            StackVariable: the stack variable if found, else None
        """
        return self.parent_node.get_stack_variable(variable_name)


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

    def __init__(self, depth, identifier, constant):
        """Create a return statement.

        Args:
            depth (int): depth in the ast tree
            identifier (str): the identifier of the symbol to return if
                              applicable
            constant (ConstantExpression): the constant expression to return
                                           if applicable
        """
        super(ReturnStatement, self).__init__(depth)
        self.id = identifier
        self.constant = constant

    def __str__(self):
        string = self._depth * '  ' + 'Return: \n'
        if self.id:
            string += self._depth * '  ' + '  ID: %s\n' % self.id
        if self.constant:
            string += self._depth * '  ' + '%s\n' % str(self.constant)
        return string

    def get_return_type(self):
        """Get the return type.

        Returns:
            str: the return type
        """
        return self.parent_node.get_return_type()

    def compile(self, assembler):
        """Compile this statement

        Args:
            assembler (Assembler)
        Returns:
            CompiledObject: the compiled version of this statement
        """
        value = bytearray()

        if self.constant:
            try:
                imm_value = int(self.constant.exp_value)
                reg = ProcessorRegister.accumulator
                value += assembler.copy_value_to_reg(imm_value, reg)
            except ValueError:
                imm_value = float(self.constant.exp_value)
                return_type = self.get_return_type()
                if return_type == 'double':
                    reg = ProcessorRegister.double_scalar_0
                else:
                    reg = ProcessorRegister.single_scalar_0
                value += assembler.copy_value_to_reg(imm_value, reg)
        elif self.id:
            return_type = self.get_return_type()
            if return_type == 'double':
                reg = ProcessorRegister.double_scalar_0
            elif return_type == 'float':
                reg = ProcessorRegister.single_scalar_0
            else:
                reg = ProcessorRegister.accumulator

            parent = self.parent_node
            id = self.id
            stack_variable = parent.get_stack_variable(id)
            stack_offset = stack_variable.stack_offset

            value += assembler.copy_stack_to_reg(stack_offset, reg)

        # restore the frame pointer from stack
        ret = assembler.pop_from_stack(ProcessorRegister.base_pointer)
        value.extend(ret)

        # return to the called function
        ret = assembler.return_to_caller()
        value.extend(ret)

        size = len(value)
        compiled_object = CompiledObject(self.id, size,
                                         value, CompiledObjectType.code)
        return compiled_object


class Expression(AstNode):
    def __init__(self, depth):
        super(Expression, self).__init__(depth)

    def __str__(self):
        string = self._depth * '  ' + 'This is an expression\n'
        return string

    def load_result_to_reg(self, register, assembler):
        """Load the result of the expression to the specified register

        Args:
            register (ProcessorRegister): the register to load the result
            assembler (Assembler): the assembler to use
        Returns:
            bytearray: the compiled code to evaluate the expression
        """
        raise NotImplementedError


class VariableReference(Expression):

    def __init__(self, depth, name):
        """Create a expression that references a variable

        Args:
            depth (int): the depth in the tree
            name (str): the name of the variable
        """
        super(VariableReference, self).__init__(depth)
        self.name = name

    def __str__(self):
        string = self._depth * '  ' + 'ID: %s\n' % self.name
        return string

    def load_result_to_reg(self, register, assembler):
        """Load the result of the expression to the specified register

        Args:
            register (ProcessorRegister): the register to load the result
            assembler (Assembler): the assembler to use
        Returns:
            bytearray: the compiled code to evaluate the expression
        """
        pass


class ConstantExpression(Expression):
    def __init__(self, exp_type, expr_value):
        self.exp_type = exp_type
        self.exp_value = expr_value

    def __str__(self):
        string = '  Constant: %s, %s' % (self.exp_type, self.exp_value)
        return string

    def load_result_to_reg(self, register, assembler):
        """Load the result of the expression to the specified register

        Args:
            register (ProcessorRegister): the register to load the result
            assembler (Assembler): the assembler to use
        Returns:
            bytearray: the compiled code to evaluate the expression
        """
        if register == ProcessorRegister.double_scalar_0 or \
                register == ProcessorRegister.double_scalar_1:
            val = float(self.exp_value)
        elif register == ProcessorRegister.single_scalar_0 or \
                register == ProcessorRegister.single_scalar_1:
            val = float(self.exp_value)
        elif register == ProcessorRegister.accumulator:
            val = int(self.exp_value)
        else:
            # all other types interpreted as int
            val = int(self.exp_value)

        value = assembler.copy_value_to_reg(val, register)

        return value


class Assignment(Statement):

    def __init__(self, depth, identifier, initializer_exp):
        """Create an assignment.

        Args:
            depth (int): the depth in the tree
            identifier (str): the variable to assign to
            initializer_exp (Expression): the expression as right hand value
        """
        super(Statement, self).__init__(depth)
        self.id = identifier
        self.initializer_exp = initializer_exp

    def __str__(self):
        string = self._depth * '  ' + 'Assignment: =\n'
        string += self._depth * '  ' + '  ID: %s\n' % self.id
        string += self._depth * '  ' + str(self.initializer_exp)
        string += '\n'
        return string

    def compile(self, assembler):
        """Compile this statement

        Args:
            assembler (Assembler)
        Returns:
            CompiledObject: the compiled version of this statement
        """
        value = bytearray()

        parent = self.parent_node
        id = self.id
        stack_variable = parent.get_stack_variable(id)
        stack_offset = stack_variable.stack_offset
        size = stack_variable.size

        if stack_variable.type_name == 'double':
            register = ProcessorRegister.double_scalar_0
        elif stack_variable.type_name == 'float':
            register = ProcessorRegister.single_scalar_0
        else:
            register = ProcessorRegister.accumulator

        value += self.initializer_exp.load_result_to_reg(register, assembler)

        value += assembler.copy_reg_to_stack(stack_offset, register)
        compiled_object = CompiledObject(self.id, size,
                                         value, CompiledObjectType.code)
        return compiled_object


class Operator:
    def __init__(self):
        pass

    def __str__(self):
        return ''


class BinaryOperator(Operator):
    def __init__(self):
        super(BinaryOperator, self).__init__()

    def __str__(self):
        return ''

    def evaluate(self, source, destination, assembler):
        """Evaluate the operator, leaving the result in the destination reg.

        Args:
            source (ProcessorRegister): the source operand
            destination (ProcessorRegister): the destination operand
            assembler (Assembler): the assembler to use
        Returns:
            bytearray: the byte code
        """
        raise NotImplementedError


class Addition(BinaryOperator):
    def __init__(self):
        super(Addition, self).__init__()

    def __str__(self):
        return '+'

    def evaluate(self, source, destination, assembler):
        """Evaluate the operator, leaving the result in the destination reg.

        Args:
            source (ProcessorRegister): the source operand
            destination (ProcessorRegister): the destination operand
            assembler (Assembler): the assembler to use
        Returns:
            bytearray: the byte code
        """
        value = bytearray()
        value += assembler.add(source, destination)
        return value


class BinaryOp(Expression):

    def __init__(self, depth, operator, operand_1, operand_2):
        """Create a binary operator

        Args:
            depth (int): the depth in the tree
            operator (BinaryOperator): the operator
            operand_1 (Expression): the first operand
            operand_2 (Expression): the second operand
        """
        super(BinaryOp, self).__init__(depth)
        self.operator = operator
        self.operand_1 = operand_1
        self.operand_2 = operand_2

    def __str__(self):
        string = (self._depth - 2) * '  ' + 'BinaryOp: %s\n' % self.operator
        string += (self._depth + 1) * '  ' + '%s\n' % self.operand_1
        string += (self._depth + 1) * '  ' + '%s' % self.operand_2
        return string

    def load_result_to_reg(self, register, assembler):
        if register == ProcessorRegister.single_scalar_0:
            register_1 = ProcessorRegister.single_scalar_0
            register_2 = ProcessorRegister.single_scalar_1
        elif register == ProcessorRegister.double_scalar_0:
            register_1 = ProcessorRegister.double_scalar_0
            register_2 = ProcessorRegister.double_scalar_1
        else:
            register_1 = ProcessorRegister.accumulator
            register_2 = ProcessorRegister.counter
        value = self.operand_1.load_result_to_reg(register_1, assembler)

        value += self.operand_2.load_result_to_reg(register_2, assembler)

        value += self.operator.evaluate(register_1, register_2, assembler)

        # the result is in register_1, make sure
        # that is the specified register
        if register != register_1:
            value += assembler.copy_from_reg_to_reg(register_1, register)

        return value
