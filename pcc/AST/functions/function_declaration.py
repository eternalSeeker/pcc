import copy

from pcc.AST.compiled_object import CompiledObject, CompiledObjectType
from pcc.AST.functions.function_argument import FunctionArgument
from pcc.AST.statement import Statement
from pcc.AST.variables.stack_variable import StackVariable
from pcc.AST.variables.variable_declaration import VariableDeclaration


class FunctionDeclaration(Statement):

    def __init__(self, return_type, name, argument_list, depth):
        """Create a function declaration

        Args:
            return_type (VariableType): the type of the return argument
            name (str): the identifier of the function
            argument_list ([FunctionArgument]): the arguments for this function
            depth (int): the depth in the tree
        """
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

    def __deepcopy__(self, memodict=None):
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
        for argument in self.argument_list:
            if isinstance(argument, FunctionArgument):
                name = argument.identifier
                if name == 'void':
                    # void arguemnts do not need to be added to the stack
                    continue
                variable_type = argument.type_decl
            elif isinstance(argument, VariableDeclaration):
                name = argument.name
                variable_type = argument.variable_type
            stack_var = StackVariable(name=name,
                                      size=variable_type.size,
                                      initializer_byte_array=bytearray(),
                                      type_name=variable_type.name)
            current_list.append(stack_var)
        # a function declaration can only hold one 1 statement,
        # a compound statement
        if len(self.statement_sequence) > 1:
            self.statement_sequence[1].add_stack_variable(current_list)

    def update_depth(self, depth):
        """Update the depth to the specified one

        Args:
            depth (int): the depth to set to
        """
        super(FunctionDeclaration, self).update_depth(depth)
        for argument in self.argument_list:
            argument.update_depth(depth + 3)

    def compile(self, _):
        """Compile this statement.

        Args:
            _ (Assembler): the assembler to use, unused but required because
                inheritance prototype.

        Returns:
            CompiledObject: the compiled version of this statement
        """
        value = bytearray()
        size = 0
        compiled_object = CompiledObject(self.name, size,
                                         value, CompiledObjectType.code)

        return compiled_object

    def get_stack_variable(self, variable_name):
        """Get the stack variable by name.

        Args:
            variable_name (str): the name of the variable

        Returns:
            StackVariable: the stack variable if found, else None
        """
        return self.parent_node.get_stack_variable(variable_name)
