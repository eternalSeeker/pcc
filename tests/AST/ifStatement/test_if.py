# -*- coding: utf-8 -*-

from os.path import abspath, dirname
from tests.AST.ASTHelper import generate_ast_outputs, ASTHelper

import pytest

import tests.generateOutputsDecorator

generate_outputs = tests.generateOutputsDecorator.generate_outputs

# The parametrize function is generated, so it does not work to import
parametrize = pytest.mark.parametrize

files_to_test = [
    'if.c',
    'else.c',
    'if_and_statements_after.c',
    'if_var_condition.c',
    'if_func_call_condition.c',
]


@generate_outputs
def generate_ast_outputs():
    folder = dirname(__file__)
    generate_ast_outputs(files_to_test, folder)


class TestIfStatement(ASTHelper):

    @parametrize('file_to_test', files_to_test)
    def test_if_statement(self, file_to_test, capsys):
        path_of_this_file = abspath(dirname(__file__))
        self.execute_test(file_to_test, capsys, path_of_this_file)
