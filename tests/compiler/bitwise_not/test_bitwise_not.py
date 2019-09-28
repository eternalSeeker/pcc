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
    ('constant.c', 'intHelper.c', 'constant.out'),
    ('variable.c', 'intHelper.c', 'variable.out'),
    ('constant_init.c', 'intHelper.c', 'constant_init.out'),
    ('variable_init.c', 'intHelper.c', 'variable_init.out'),
]


@generate_outputs
def generate_compiler_test_outputs():
    path_of_this_file = abspath(dirname(__file__))
    generate_compiler_outputs(files_to_test, path_of_this_file)


class TestBitwiseNot(CompilerHelper):

    @parametrize('file_to_test,helper,output_file', files_to_test)
    def test_bitwise_not(self, file_to_test, helper, output_file, capsys):
        path_of_this_file = abspath(dirname(__file__))
        self.execute_test(file_to_test, helper, output_file, capsys,
                          path_of_this_file)
