from pcc.AST.ast_node import push_variable_on_stack
from pcc.AST.compiled_object import CompiledObjectType, CompiledObject
from pcc.AST.functions.function_argument import FunctionArgument
from pcc.AST.functions.function_declaration import FunctionDeclaration
from pcc.AST.statement import Statement
from pcc.AST.variables.variable_declaration import VariableDeclaration
from pcc.compiler.assembler import ProcessorRegister


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

        Returns:
            FunctionDefinition: self

        """
        return self

    def add_stack_variable(self, current_list):
        """Add all stack variable to the list.

        Args:
            current_list (list[StackVariable]): the current list
        """
        for statement in self.statement_sequence:
            statement.add_stack_variable(current_list)

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

    def _copy_argmuments_to_stack(self, assembler):
        """Copy all the arguments of this function to their stack variables.

        Args:
            assembler (Assembler): the assembler to use

        Returns:
            bytearray: the compiled machine code

        """
        compiled_code = bytearray()
        function_definition: FunctionDeclaration = self.statement_sequence[0]
        available_integer_registers = [
            ProcessorRegister.integer_argument_0,
            ProcessorRegister.integer_argument_1,
            ProcessorRegister.integer_argument_2,
            ProcessorRegister.integer_argument_3,
            ProcessorRegister.integer_argument_4,
            ProcessorRegister.integer_argument_5]
        for argument in function_definition.argument_list:
            if isinstance(argument, FunctionArgument):
                stack_var = self.get_stack_variable(argument.identifier)
            elif isinstance(argument, VariableDeclaration):
                stack_var = self.get_stack_variable(argument.name)
            if not stack_var and argument.identifier == 'void':
                continue
            stack_offset = stack_var.stack_offset
            if stack_var.type_name not in ['float', 'double']:
                register = available_integer_registers.pop(0)
            compiled_code += \
                assembler.copy_reg_to_stack(register=register,
                                            stack_offset=stack_offset)

        return compiled_code

    def compile(self, assembler):
        """Compile this statement.

        Args:
            assembler (Assembler): the assembler to use

        Returns:
            CompiledObject: the compiled version of this statement
        """
        value = bytearray()

        # save the frame pointer on stack
        ret = assembler.push_to_stack(ProcessorRegister.base_pointer)
        value.extend(ret)

        # set the stack pointer as the new base pointer
        dest = ProcessorRegister.base_pointer
        src = ProcessorRegister.frame_pointer
        ret = assembler.copy_from_reg_to_reg(destination=dest,
                                             source=src)
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
                                                         value,
                                                         value_array)
            stack_var.stack_offset = stack_offset

        self.stack_variable_list = current_list

        # add a nop
        ret = assembler.nop()
        value.extend(ret)

        value += self._copy_argmuments_to_stack(assembler)

        relocation_objects = []
        for statement in self.statement_sequence:
            compiled_object = statement.compile(assembler)
            if compiled_object is None:
                continue
            reloc_objects = compiled_object.relocation_objects
            for relocation_object in reloc_objects:
                additional_offset = len(value)
                relocation_object.offset += additional_offset
                relocation_objects.append(relocation_object)
            value += compiled_object.value

        size = len(value)
        compiled_object = CompiledObject(self.statement_sequence[0].name, size,
                                         value, CompiledObjectType.code,
                                         relocation_objects)

        return compiled_object
