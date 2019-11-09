#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pcc.AST.ast_node import AstNode
from pcc.compiler.assembler_x64 import X64Assembler
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
        self.assembler = X64Assembler()

    def compile(self):
        """Compile the AST.

        """
        if not isinstance(self.ast_root_node, AstNode):
            return
        for statement in self.ast_root_node.statement_sequence:
            compiled_object = statement.compile(self.assembler)
            if compiled_object:
                symbol = Symbol(compiled_object.name, compiled_object.value,
                                compiled_object.size, compiled_object.type,
                                compiled_object.relocation_objects)
                self.object_file.add_symbol(symbol)

    def write_object_file_to_file(self, file_name):
        """Write the object file to a binary file.

        Args:
            file_name (str): the file name with path for the object file
        """
        with open(file_name, 'wb+') as file:
            file.write(self.object_file.to_binary_array())
