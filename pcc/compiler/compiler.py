#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pcc.AST.ast import AstNode, CompiledObjectType
from pcc.compiler.objectFile import ObjectFile, Symbol


class Compiler:

    def __init__(self, input_file_name, ast_root_node):
        """Create a compiler object.

        Args:
            input_file_name (str): the file name as string
            ast_root_node (AstNode): the root node of the ast
        """

        self.input_file_name = input_file_name
        self.ast_root_node = ast_root_node
        self.object_file = ObjectFile(self.input_file_name)

    def compile(self):
        """Compile the AST.

        """
        if not isinstance(self.ast_root_node, AstNode):
            return
        for statement in self.ast_root_node.statement_sequence:
            compiled_opject = statement.compile()
            if compiled_opject:
                is_text = False
                if compiled_opject.type == CompiledObjectType.code:
                    is_text = True
                symbol = Symbol(compiled_opject.name, compiled_opject.value,
                                compiled_opject.size, is_text)
                self.object_file.add_symbol(symbol)

    def write_object_file_to_file(self, file_name):
        """Write the object file to a binary file.

        Args:
            file_name (str): the file name with path for the object file
        """
        with open(file_name, 'wb+') as file:
            file.write(self.object_file.to_binary_array())
