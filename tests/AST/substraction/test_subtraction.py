# -*- coding: utf-8 -*-

from os.path import abspath, dirname
from tests.AST.ASTHelper import generate_ast_outputs, ASTHelper

import pytest

import tests.generateOutputsDecorator

generate_outputs = tests.generateOutputsDecorator.generate_outputs

# The parametrize function is generated, so it does not work to import
parametrize = pytest.mark.parametrize

files_to_test = [
    'intInit.c',
    'charInit.c',
    'floatInit.c',
    'doubleInit.c',
    'intConstant.c',
    'charConstant.c',
    'floatConstant.c',
    'doubleConstant.c',
    'intConstantAndVar.c',
    'charConstantAndVar.c',
    'floatConstantAndVar.c',
    'doubleConstantAndVar.c',
]


@generate_outputs
def generate_ast_test_outputs():
    folder = dirname(__file__)
    generate_ast_outputs(files_to_test, folder)


class TestSubtraction(ASTHelper):

    @parametrize('file_to_test', files_to_test)
    def test_subtraction(self, file_to_test, capsys):
        path_of_this_file = abspath(dirname(__file__))
        self.execute_test(file_to_test, capsys, path_of_this_file)
