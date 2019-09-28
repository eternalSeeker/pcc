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
    ('returnVoid.c', 'voidHelper.c', 'returnVoid.out'),
    ('returnChar.c', 'charHelper.c', 'returnChar.out'),
    ('returnInt.c', 'intHelper.c', 'returnInt.out'),
    ('returnFloat.c', 'floatHelper.c', 'returnFloat.out'),
    ('returnDouble.c', 'doubleHelper.c', 'returnDouble.out'),
    ('returnVarInt.c', 'intHelper.c', 'returnVarInt.out'),
    ('returnVarChar.c', 'charHelper.c', 'returnVarChar.out'),
    ('returnVarFloat.c', 'floatHelper.c', 'returnVarFloat.out'),
    ('returnVarDouble.c', 'doubleHelper.c', 'returnVarDouble.out'),
]


@generate_outputs
def generate_compiler_test_outputs():
    path_of_this_file = abspath(dirname(__file__))
    generate_compiler_outputs(files_to_test, path_of_this_file)


class TestReturnStatement(CompilerHelper):

    @parametrize('file_to_test,helper,output_file', files_to_test)
    def test_return_statement(self, file_to_test, helper,
                              output_file, capsys):
        path_of_this_file = abspath(dirname(__file__))
        self.execute_test(file_to_test, helper, output_file, capsys,
                          path_of_this_file)
