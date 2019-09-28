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
    ('constant_true.c', 'intHelper.c', 'constant_true.out'),
    ('constant_false.c', 'intHelper.c', 'constant_false.out'),
    ('variable_true.c', 'intHelper.c', 'variable_true.out'),
    ('variable_false.c', 'intHelper.c', 'variable_false.out'),
    ('constant_true_else.c', 'intHelper.c', 'constant_true_else.out'),
    ('constant_false_else.c', 'intHelper.c', 'constant_false_else.out'),
    ('variable_true_else.c', 'intHelper.c', 'variable_true_else.out'),
    ('variable_false_else.c', 'intHelper.c', 'variable_false_else.out'),
]


@generate_outputs
def generate_compiler_test_outputs():
    path_of_this_file = abspath(dirname(__file__))
    generate_compiler_outputs(files_to_test, path_of_this_file)


class TestIf(CompilerHelper):

    @parametrize('file_to_test,helper,output_file', files_to_test)
    def test_if(self, file_to_test, helper, output_file, capsys):
        path_of_this_file = abspath(dirname(__file__))
        self.execute_test(file_to_test, helper, output_file, capsys,
                          path_of_this_file)
