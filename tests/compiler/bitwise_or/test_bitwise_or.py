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
    ('constant_constant.c', 'intHelper.c', 'constant_constant.out'),
    ('variable_constant.c', 'intHelper.c', 'variable_constant.out'),
    ('constant_variable.c', 'intHelper.c', 'constant_variable.out'),
    ('variable_variable.c', 'intHelper.c', 'variable_variable.out'),
    ('constant_constant_init.c', 'intHelper.c', 'constant_constant_init.out'),
    ('variable_constant_init.c', 'intHelper.c', 'variable_constant_init.out'),
    ('constant_variable_init.c', 'intHelper.c', 'constant_variable_init.out'),
    ('variable_variable_init.c', 'intHelper.c', 'variable_variable_init.out'),
]


@generate_outputs
def generate_compiler_test_outputs():
    path_of_this_file = abspath(dirname(__file__))
    generate_compiler_outputs(files_to_test, path_of_this_file)


class TestBitwiseOr(CompilerHelper):

    @parametrize('file_to_test,helper,output_file', files_to_test)
    def test_bitwise_or(self, file_to_test, helper, output_file, capsys):
        path_of_this_file = abspath(dirname(__file__))
        self.execute_test(file_to_test, helper, output_file, capsys,
                          path_of_this_file)
