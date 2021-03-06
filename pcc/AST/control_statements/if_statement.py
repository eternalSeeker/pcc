from pcc.AST.compiled_object import CompiledObjectType, CompiledObject
from pcc.AST.statement import Statement
from pcc.compiler.assembler import ProcessorRegister


class IfStatement(Statement):

    def __init__(self, depth, condition, if_statement, else_statement=None):
        """Create an if statement.

        Args:
            depth (int): depth in the ast tree
            condition (Union[pcc.AST.expression.Expression,None]): the
                conditional to evaluate to true to jump to the if branch
                else the else
            if_statement (pcc.AST.Statement): the if branch
            else_statement (Union[pcc.AST.Statement, None]): the if branch
        """
        super(IfStatement, self).__init__(depth)
        self.condition = condition
        self.if_statement = if_statement
        self.else_statement = else_statement

    def __str__(self):
        string = self._depth * '  ' + 'If: \n'
        string += '%s\n' % str(self.condition)
        string += '%s' % str(self.if_statement)
        if self.else_statement:
            string += '%s' % str(self.else_statement)
        return string

    def compile(self, assembler):
        """Compile this statement

        Args:
            assembler (Assembler): the assembler to use

        Returns:
            CompiledObject: the compiled version of this statement
        """
        value = bytearray()

        if_part = self.if_statement.compile(assembler)

        # compare the value from the condition, to 0. If not equal,
        # go to the if part, else to the else part if present.
        condition_reg = ProcessorRegister.accumulator
        condition_code, relocation_objects = \
            self.condition.load_result_to_reg(condition_reg, assembler)
        value += condition_code

        compare_register = ProcessorRegister.counter
        value_to_load = 0
        value += assembler.copy_value_to_reg(value_to_load, compare_register)

        value += assembler.cmp(condition_reg, compare_register)

        jump_distance = len(if_part.value)
        if self.else_statement:
            else_part = self.else_statement.compile(assembler)
            jump_distance_else = len(else_part.value)
            # if there if an else part, the last instruction of the if part
            # is the jump over the else part.
            jump_distance += len(assembler.jmp(jump_distance_else))

        value += assembler.je(jump_distance)
        for relocation_object in if_part.relocation_objects:
            additional_offset = len(value)
            relocation_object.offset += additional_offset
            relocation_objects.append(relocation_object)
        value += if_part.value

        if self.else_statement:
            # jump over the else part (for the if part)
            value += assembler.jmp(jump_distance_else)
            for relocation_object in else_part.relocation_objects:
                additional_offset = len(value)
                relocation_object.offset += additional_offset
                relocation_objects.append(relocation_object)
            # the actual else part
            value += else_part.value

        size = len(value)
        compiled_object = CompiledObject('if', size,
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

    def get_return_type(self):
        """Get the return type.

        Returns:
            str: the return type
        """
        return self.parent_node.get_return_type()

    def add_stack_variable(self, current_list):
        """Add all stack variable to the list

        Args:
            current_list(list[StackVariable]): the current list
        """
        self.if_statement.add_stack_variable(current_list)
        if self.else_statement:
            self.else_statement.add_stack_variable(current_list)
