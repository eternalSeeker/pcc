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
    ('char.c', 'charHelper.c', 'char.out'),
    ('int.c', 'intHelper.c', 'int.out'),
    ('float.c', 'floatHelper.c', 'float.out'),
    ('double.c', 'doubleHelper.c', 'double.out'),
    ('charInit.c', 'charHelper.c', 'charInit.out'),
    ('intInit.c', 'intHelper.c', 'intInit.out'),
    ('floatInit.c', 'floatHelper.c', 'floatInit.out'),
    ('doubleInit.c', 'doubleHelper.c', 'doubleInit.out'),
    ('charVarAndConstant.c', 'charHelper.c', 'charVarAndConstant.out'),
    ('intVarAndConstant.c', 'intHelper.c', 'intVarAndConstant.out'),
    ('floatVarAndConstant.c', 'floatHelper.c', 'floatVarAndConstant.out'),
    ('doubleVarAndConstant.c', 'doubleHelper.c', 'doubleVarAndConstant.out'),
]


@generate_outputs
def generate_compiler_test_outputs():
    path_of_this_file = abspath(dirname(__file__))
    generate_compiler_outputs(files_to_test, path_of_this_file)


class TestMultiplication(CompilerHelper):

    @parametrize('file_to_test,helper,output_file', files_to_test)
    def test_multiplication(self, file_to_test, helper, output_file, capsys):
        path_of_this_file = abspath(dirname(__file__))
        self.execute_test(file_to_test, helper, output_file, capsys,
                          path_of_this_file)
