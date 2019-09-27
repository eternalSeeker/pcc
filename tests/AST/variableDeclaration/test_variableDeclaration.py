# -*- coding: utf-8 -*-

from os.path import abspath, dirname
from tests.AST.ASTHelper import generate_ast_outputs, ASTHelper

import pytest

import tests.generateOutputsDecorator

generate_outputs = tests.generateOutputsDecorator.generate_outputs

# The parametrize function is generated, so it does not work to import
parametrize = pytest.mark.parametrize

files_to_test = [
    'oneGlobalVariable.c',
    'twoGlobalVariables.c',
    'allTypes.c',
    'variableInitialisation.c',
    'combinedDeclaration.c',
    'combinedDeclarationWithInitializer.c',
    'charArray.c',
    'charArraySize.c',
    'charArrayInitialization.c',
    'charArraySizeInitialization.c',
    'variableComplexInitialisation.c',
]


@generate_outputs
def generate_ast_outputs():
    folder = dirname(__file__)
    generate_ast_outputs(files_to_test, folder)


class TestConditionalCompilation(ASTHelper):

    @parametrize('file_to_test', files_to_test)
    def test_variableDeclaration(self, file_to_test, capsys):
        path_of_this_file = abspath(dirname(__file__))
        self.execute_test(file_to_test, capsys, path_of_this_file)
