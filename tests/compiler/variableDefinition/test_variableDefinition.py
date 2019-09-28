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
    ('charNoInit.c', 'charNoInit_helper.c', 'charNoInit.out'),
    ('charOne.c', 'char_helper.c', 'charOne.out'),
    ('charMax.c', 'char_helper.c', 'charMax.out'),
    ('charMin.c', 'char_helper.c', 'charMin.out'),
    ('intNoInit.c', 'intNoInit_helper.c', 'intNoInit.out'),
    ('intOne.c', 'int_helper.c', 'intOne.out'),
    ('intMinOne.c', 'int_helper.c', 'intMinOne.out'),
    ('intBig.c', 'int_helper.c', 'intBig.out'),
    ('intBigNeg.c', 'int_helper.c', 'intBigNeg.out'),
    ('floatNoInit.c', 'floatNoInit_helper.c', 'floatNoInit.out'),
    ('floatOne.c', 'float_helper.c', 'floatOne.out'),
    ('floatBig.c', 'float_helper.c', 'floatBig.out'),
    ('floatSmallPos.c', 'float_helper.c', 'floatSmallPos.out'),
    ('floatVeryNeg.c', 'float_helper.c', 'floatVeryNeg.out'),
    ('doubleNoInit.c', 'doubleNoInit_helper.c', 'doubleNoInit.out'),
    ('doubleOne.c', 'double_helper.c', 'doubleOne.out'),
    ('doubleBig.c', 'double_helper.c', 'doubleBig.out'),
    ('doubleSmallPos.c', 'double_helper.c', 'doubleSmallPos.out'),
    ('doubleVeryNeg.c', 'double_helper.c', 'doubleVeryNeg.out'),
]


@generate_outputs
def generate_compiler_test_outputs():
    path_of_this_file = abspath(dirname(__file__))
    generate_compiler_outputs(files_to_test, path_of_this_file)


class TestVariableDefinition(CompilerHelper):

    @parametrize('file_to_test,helper,output_file', files_to_test)
    def test_variable_definition(self, file_to_test, helper,
                                 output_file, capsys):
        path_of_this_file = abspath(dirname(__file__))
        self.execute_test(file_to_test, helper, output_file, capsys,
                          path_of_this_file)
