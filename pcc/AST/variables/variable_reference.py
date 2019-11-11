from pcc.AST.compiled_object import CompiledObjectType
from pcc.AST.expression import Expression
from pcc.compiler.relocation_object import RelocationObject


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
        string = (self._depth + 1) * '  ' + 'ID: %s' % self.name
        return string

    def load_result_to_reg(self, register, assembler):
        """Load the result of the expression to the specified register

        Args:
            register (ProcessorRegister): the register to load the result
            assembler (Assembler): the assembler to use

        Returns:
            bytearray: the compiled code to evaluate the expression
            List[RelocationObject]: the required relocation objects
        """
        value = bytearray()
        parent = self.parent_node
        identifier = self.name
        stack_variable = parent.get_stack_variable(identifier)
        relocation_objects = []
        if stack_variable is not None:
            stack_offset = stack_variable.stack_offset
            value += assembler.copy_stack_to_reg(stack_offset, register)
        else:
            node = self.get_global_symbol(identifier)
            compiled_code, displacement_offset = \
                assembler.mov_from_displacement(register, displacement=0)
            offset = len(value) + displacement_offset
            value += compiled_code
            # the offset in the symbol is 4
            addend = -4
            relocation_object = RelocationObject(node.name, offset,
                                                 CompiledObjectType.data,
                                                 addend)
            relocation_objects.append(relocation_object)

        return value, relocation_objects
