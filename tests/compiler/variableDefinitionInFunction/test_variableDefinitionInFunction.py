# -*- coding: utf-8 -*-

from os.path import abspath, dirname

import pytest

import tests.generateOutputsDecorator
from tests.compiler.CompilerHelper import CompilerHelper, \
    generate_compiler_outputs

generate_outputs = tests.generateOutputsDecorator.generate_outputs

# The parametrize function is generated, so it does not work to import
parametrize = pytest.mark.parametrize

files_to_test = [
    ('int.c', 'helper.c', 'int.out'),
    ('char.c', 'helper.c', 'char.out'),
    ('float.c', 'helper.c', 'float.out'),
    ('double.c', 'helper.c', 'double.out'),
]


@generate_outputs
def generate_compiler_test_outputs():
    path_of_this_file = abspath(dirname(__file__))
    generate_compiler_outputs(files_to_test, path_of_this_file)


class TestVariableDefinitionInFunction(CompilerHelper):

    @parametrize('file_to_test,helper,output_file', files_to_test)
    def test_return_statement(self, file_to_test, helper,
                              output_file, capsys):
        path_of_this_file = abspath(dirname(__file__))
        self.execute_test(file_to_test, helper, output_file, capsys,
                          path_of_this_file)
