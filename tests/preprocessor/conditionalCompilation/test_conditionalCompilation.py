# -*- coding: utf-8 -*-
from tests.preprocessor.preprocessorhelper import PreprocessorHelper
from ...preprocessor.preprocessorhelper import generate_preprocessor_outputs

from os.path import abspath, dirname
import pytest

import tests.generateOutputsDecorator

# The parametrize function is generated, so it does not work to import
parametrize = pytest.mark.parametrize
generate_outputs = tests.generateOutputsDecorator.generate_outputs

files_to_test = [
    'constantExpression.c',
    'constantExpression_OR.c',
    'nested.c',
    'simple.c',
    'constantExpression_0.c',
    'else.c',
    # 'nested_else.c'
]


@generate_outputs
def generate_ast_outputs():
    """Generate the output for the tests.

    """
    folder = dirname(__file__)
    generate_preprocessor_outputs(files_to_test, folder)


class TestConditionalCompilation(PreprocessorHelper):

    @parametrize('file_to_test', files_to_test)
    def test_conditional_compilation(self, file_to_test, capsys):
        """Execute the conditional compilation test.

        Args:
            file_to_test (str): the file to test
            capsys (method): the capsys fixture from pytest
        """
        path_of_this_file = abspath(dirname(__file__))
        self.execute_test(file_to_test, capsys, path_of_this_file)
