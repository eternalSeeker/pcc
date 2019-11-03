import struct

from pcc.AST.compiled_object import CompiledObjectType, CompiledObject
from pcc.AST.functions.function_argument import FunctionArgument
from pcc.AST.variables.stack_variable import StackVariable
from pcc.AST.statement import Statement
from pcc.compiler.assembler import ProcessorRegister


class VariableDeclaration(Statement):

    def __init__(self, variable_type, name, initializer,
                 depth, is_extern=False):
        """Create a variable declaration.

        Args:
            variable_type (pcc.AST.ast.VariableType): the type
            name (str): the name of the variable
            initializer (pcc.AST.expression.Expression): the expression
                to initialize
            depth (int): the depth in the tree
            is_extern (bool): True if this is an external variable
        """
        super(VariableDeclaration, self).__init__(depth)
        self.variable_type = variable_type
        self.name = name
        self.initializer = initializer
        self.stack_var = None
        self.is_extern = is_extern

    def __str__(self):
        external = '\'extern\'' if self.is_extern is True else ''
        string = self._depth * '  ' + 'Decl: ' + self.name
        string += ', [], [' + external + '], []\n'
        string += self._depth * '  ' + '  TypeDecl: ' + self.name + ', []\n'
        string += self._depth * '  ' + '    IdentifierType: [\'' \
            + self.variable_type.name + '\']\n'
        if self.initializer:
            string += str(self.initializer) + '\n'
        return string

    def is_compatible_to(self, variable_declaration):
        """Check if this variable declaration is compatible.

        Args:
            variable_declaration (VariableDeclaration): the variable to
                compare to

        Returns:
            bool: if the object is compatible
        """
        if isinstance(variable_declaration, FunctionArgument):
            if self.variable_type.name == variable_declaration.type_name:
                return True
            elif self.variable_type.name == 'void' and \
                    variable_declaration.type_name is None:
                return True
            else:
                return False
        if self.variable_type == variable_declaration.variable_type:
            return True
        return False

    def compile(self, assembler):
        """Compile this statement

        Args:
            assembler (Assembler): the assembler to use

        Returns:
            CompiledObject: the compiled version of this statement
        """
        size = self.variable_type.size
        value = bytearray()
        if self.is_extern:
            size = 0
            compiled_object = CompiledObject(self.name, size, value,
                                             CompiledObjectType.data)
        else:
            compiled_object = self.compile_internal_variable(assembler, size)

        return compiled_object

    def compile_internal_variable(self, assembler, size):
        """Compile a non-external variable

        Args:
            assembler (Assembler): the assembler to use
            size (int): the size of the type of this variable

        Returns:
            CompiledObject: the compiled version of this variable
        """
        value = bytearray()
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
