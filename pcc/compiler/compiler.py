#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pcc.AST.ast import AstNode
from pcc.compiler.objectFile import ObjectFile, Symbol


class Compiler:

    def __init__(self, ast_root_node):
        """Create a compiler object.

        Args:
            ast (AstNode): the root node of the ast
        """

        self.ast_root_node = ast_root_node
        self.object_file = ObjectFile()

    def compile(self):
        if not isinstance(self.ast_root_node, AstNode):
            return
        for statement in self.ast_root_node.statement_sequence:
            compiled_opject = statement.compile()
            symbol = Symbol(compiled_opject.name, compiled_opject.value)
            self.object_file.add_symbol(symbol)

    def write_object_file_to_file(self, file_name):
        with open(file_name, 'wb+') as file:
            file.write(self.object_file.to_binary_array())