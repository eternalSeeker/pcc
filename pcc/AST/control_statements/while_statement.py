from pcc.AST.compiled_object import CompiledObjectType, CompiledObject
from pcc.AST.statement import Statement
from pcc.compiler.assembler import ProcessorRegister


class WhileStatement(Statement):

    def __init__(self, depth, condition, body_statement):
        """Create a while statement.

        Args:
            depth (int): depth in the ast tree
            condition (pcc.AST.expression.Expression): the conditional to
                evaluate for the while loop
            body_statement (pcc.AST.Statement): the expression to loop over
        """
        super(WhileStatement, self).__init__(depth)
        self.condition = condition
        self.body_statement = body_statement

    def __str__(self):
        string = self._depth * '  ' + 'While: \n'
        string += '%s\n' % str(self.condition)
        string += '%s' % str(self.body_statement)
        return string

    def compile(self, assembler):
        """Compile this statement

        Args:
            assembler (Assembler): the assembler to use

        Returns:
            CompiledObject: the compiled version of this statement
        """
        value = bytearray()

        body_part = self.body_statement.compile(assembler)

        # compare the value from the condition, to 0. If not equal,
        # go to the if part, else to the else part if present.
        condition_reg = ProcessorRegister.accumulator
        condition_code, relocation_objects = \
            self.condition.load_result_to_reg(condition_reg, assembler)
        value += condition_code

        body_len = len(body_part.value)

        # the distance over the body is the length of the body as well as the
        # jump back at the end. Just encode a random length to calc this length
        jump_over_body = body_len + len(assembler.jmp(body_len))

        value += assembler.cmp_against_const(condition_reg, const=0)
        value += assembler.je(jump_over_body)

        len_condition = len(value)

        value += body_part.value
        # the distance to jump back, is the relative distance after the jump
        # instruction. So the complete distance is the length of the body,
        # the length of the condition and this jump (use the length of a
        # random jump to know the length)
        jump_back_dist = -len_condition - body_len - \
            len(assembler.jmp(0))
        value += assembler.jmp(jump_back_dist)

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
