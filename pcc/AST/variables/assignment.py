import pcc
from pcc.AST.compiled_object import CompiledObjectType, CompiledObject
from pcc.AST.statement import Statement
from pcc.compiler.assembler import ProcessorRegister
from pcc.compiler.relocation_object import RelocationObject


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
        if self.initializer_exp:
            self.initializer_exp.parent_node = self

    def __str__(self):
        string = self._depth * '  ' + 'Assignment: =\n'
        string += self._depth * '  ' + '  ID: %s\n' % self.id
        string += str(self.initializer_exp)
        string += '\n'
        return string

    def compile(self, assembler):
        """Compile this statement

        Args:
            assembler (Assembler): the assembler to use

        Returns:
            CompiledObject: the compiled version of this statement
        """

        parent = self.parent_node
        identifier = self.id
        stack_variable = parent.get_stack_variable(identifier)
        if stack_variable is None:
            compiled_object = self.compile_global_variable(assembler,
                                                           identifier)
        else:
            compiled_object = self.compile_stack_variable(assembler,
                                                          stack_variable)
        return compiled_object

    def compile_stack_variable(self, assembler, stack_variable):
        """Compile an assignment of an stack variable.

        Args:
            assembler (Assembler): the assembler to use
            stack_variable (StackVariable): the retrieved stack variable

        Returns:
            CompiledObject: the compiled version of this assignment
        """
        value = bytearray()
        stack_offset = stack_variable.stack_offset
        size = stack_variable.size
        if stack_variable.type_name == 'double':
            register = ProcessorRegister.double_scalar_0
        elif stack_variable.type_name == 'float':
            register = ProcessorRegister.single_scalar_0
        else:
            register = ProcessorRegister.accumulator
        compiled_code, relocation_objects = \
            self.initializer_exp.load_result_to_reg(register, assembler)
        for relocation_object in relocation_objects:
            additional_offset = len(value)
            relocation_object.offset += additional_offset
        value += compiled_code
        value += assembler.copy_reg_to_stack(stack_offset, register)
        compiled_object = CompiledObject(self.id, size,
                                         value, CompiledObjectType.code,
                                         relocation_objects)
        return compiled_object

    def compile_global_variable(self, assembler, identifier):
        """Compile an assignment of an stack variable.

        Args:
            assembler (Assembler): the assembler to use
            identifier (str): the identifier of the resulting variable

        Returns:
            CompiledObject: the compiled version of this assignment
        """
        value = bytearray()
        node = self.get_global_symbol(identifier)
        if node is None:
            file_name = 'unknown'
            line_number = -1
            message = f'could not fine the identifier {identifier}'
            pcc.utils.warning.error(file_name, line_number, message)
            return None
        variable_type = node.variable_type
        if variable_type.name == 'double':
            register = ProcessorRegister.double_scalar_0
        elif variable_type.name == 'float':
            register = ProcessorRegister.single_scalar_0
        else:
            register = ProcessorRegister.accumulator

        compiled_code, relocation_objects = \
            self.initializer_exp.load_result_to_reg(register, assembler)

        value += compiled_code

        # use a 0 displacement as the linker will fill it in
        compiled_code, displacement_offset = \
            assembler.mov_to_displacement(register, displacement=0)
        offset = len(value) + displacement_offset
        value += compiled_code
        # the offset in the symbol is 4
        addend = -4
        size = len(value)
        relocation_object = RelocationObject(node.name, offset,
                                             CompiledObjectType.data, addend)
        relocation_objects.append(relocation_object)
        compiled_object = CompiledObject(self.id, size,
                                         value, CompiledObjectType.code,
                                         relocation_objects)

        return compiled_object

    def get_stack_variable(self, variable_name):
        """Get the stack variable by name.

        Args:
            variable_name (str): the name of the variable

        Returns:
            StackVariable: the stack variable if found, else None
        """
        return self.parent_node.get_stack_variable(variable_name)
