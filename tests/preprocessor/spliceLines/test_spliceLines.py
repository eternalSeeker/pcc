# -*- coding: utf-8 -*-

from os.path import abspath, dirname

# The parametrize function is generated, so it does not work to import
import pytest

import tests.generateOutputsDecorator
from tests.preprocessor.preprocessorhelper import \
    generate_preprocessor_outputs, PreprocessorHelper

parametrize = pytest.mark.parametrize
generate_outputs = tests.generateOutputsDecorator.generate_outputs

files_to_test = [
    'linesplicing_1.c'
]


@generate_outputs
def generate_ast_outputs():
    """Generate the output for the tests.

    """
    folder = dirname(__file__)
    generate_preprocessor_outputs(files_to_test, folder)


class TestLineSplicing(PreprocessorHelper):

    @parametrize('file_to_test', files_to_test)
    def test_line_splicing(self, file_to_test, capsys):
        """Execute the line splicing test.

        Args:
            file_to_test (str): the file to test
            capsys (method): the capsys fixture from pytest
        """
        path_of_this_file = abspath(dirname(__file__))
        self.execute_test(file_to_test, capsys, path_of_this_file)
