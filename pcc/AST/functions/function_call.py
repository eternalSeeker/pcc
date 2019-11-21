from pcc.AST.compiled_object import CompiledObjectType, CompiledObject
from pcc.AST.expression import Expression
from pcc.AST.statement import Statement
from pcc.compiler.assembler import ProcessorRegister
from pcc.compiler.relocation_object import RelocationObject


class FunctionCall(Statement, Expression):

    def __init__(self, depth, identifier, expression_list=None):
        super(FunctionCall, self).__init__(depth)
        if expression_list is None:
            expression_list = []
        self.id = identifier
        self.expression_list = expression_list

    def __str__(self):
        string = self._depth * '  ' + 'FuncCall: \n'
        string += self._depth * '  ' + '  ID: %s\n' % self.id
        if self.expression_list:
            string += self._depth * '  ' + '  ExprList: \n'
            for expression in self.expression_list:
                string += "%s\n" % str(expression)
        index = string.rfind('\n')
        string = string[:index] + string[index+1:]
        return string

    def get_stack_variable(self, variable_name):
        """Get the stack variable by name.

        Args:
            variable_name (str): the name of the variable

        Returns:
            StackVariable: the stack variable if found, else None
        """
        return self.parent_node.get_stack_variable(variable_name)

    def load_result_to_reg(self, register, assembler):
        pass

    def update_parent(self):
        for expression in self.expression_list:
            expression.parent_node = self

    def _copy_argmuments_to_registers(self, assembler):
        """Copy all the arguments of this function to their registers.

        Args:
            assembler (Assembler): the assembler to use

        Returns:
            bytearray: the compiled machine code
            list[RelocationObject]: the used relocation objects

        """
        compiled_code = bytearray()
        relocation_objects = []
        available_integer_registers = [
            ProcessorRegister.integer_argument_0,
            ProcessorRegister.integer_argument_1,
            ProcessorRegister.integer_argument_2,
            ProcessorRegister.integer_argument_3,
            ProcessorRegister.integer_argument_4,
            ProcessorRegister.integer_argument_5]
        for expression in self.expression_list:
            register = available_integer_registers.pop(0)
            tmp_reg = ProcessorRegister.accumulator
            if tmp_reg == register:
                tmp_reg = ProcessorRegister.counter
            compiled, rela_objs = \
                expression.load_result_to_reg(assembler=assembler,
                                              register=tmp_reg)
            # update the offsets
            for obj in rela_objs:
                additional_offset = len(compiled_code)
                obj.offset += additional_offset
                relocation_objects.append(obj)
            compiled_code += compiled
            compiled_code += \
                assembler.copy_from_reg_to_reg(source=tmp_reg,
                                               destination=register)

        return compiled_code, relocation_objects

    def compile(self, assembler):
        """Compile this statement

        Args:
            assembler (Assembler): the assembler to use

        Returns:
            CompiledObject: the compiled version of this statement
        """
        pass
        value = bytearray()
        relocation_objects = []

        # load all variables in the registers
        compiled_code, rela_objs = \
            self._copy_argmuments_to_registers(assembler)
        relocation_objects += rela_objs
        value += compiled_code

        node = self.get_global_symbol(self.id)
        compiled_code, displacement_offset = \
            assembler.call(displacement=0)
        offset = len(value) + displacement_offset
        value += compiled_code
        # the offset in the symbol is 4
        addend = -4
        relocation_object = RelocationObject(node.name, offset,
                                             CompiledObjectType.code,
                                             addend)
        relocation_objects.append(relocation_object)

        size = len(value)
        compiled_object = CompiledObject(self.id, size,
                                         value, CompiledObjectType.code,
                                         relocation_objects)

        return compiled_object
