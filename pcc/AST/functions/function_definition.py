from pcc.AST.ast_node import push_variable_on_stack
from pcc.AST.compiled_object import CompiledObjectType, CompiledObject
from pcc.AST.statement import Statement
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
            assembler (Assembler): the assembler to use

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
