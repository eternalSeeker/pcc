from pcc.AST.compiled_object import CompiledObjectType, CompiledObject
from pcc.AST.expression import Expression
from pcc.AST.statement import Statement
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

    def load_result_to_reg(self, register, assembler):
        pass

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
