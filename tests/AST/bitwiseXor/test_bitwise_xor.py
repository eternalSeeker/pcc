# -*- coding: utf-8 -*-

from os.path import abspath, dirname
from tests.AST.ASTHelper import generate_ast_outputs, ASTHelper

import pytest

import tests.generateOutputsDecorator

generate_outputs = tests.generateOutputsDecorator.generate_outputs

# The parametrize function is generated, so it does not work to import
parametrize = pytest.mark.parametrize

files_to_test = [
    'constant_constant.c',
    'constant_variable.c',
    'variable_constant.c',
    'variable_variable.c',
    'constant_constant_init.c',
    'constant_variable_init.c',
    'variable_constant_init.c',
    'variable_variable_init.c',
]


@generate_outputs
def generate_ast_test_outputs():
    folder = dirname(__file__)
    generate_ast_outputs(files_to_test, folder)


class TestBitwiseOr(ASTHelper):

    @parametrize('file_to_test', files_to_test)
    def test_bitwise_xor(self, file_to_test, capsys):
        path_of_this_file = abspath(dirname(__file__))
        self.execute_test(file_to_test, capsys, path_of_this_file)
