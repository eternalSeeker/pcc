# -*- coding: utf-8 -*-

from os.path import abspath, dirname

# The parametrize function is generated, so it does not work to import
import pytest

import tests.generateOutputsDecorator
from pcc.main import main
from tests.preprocessor.preprocessorhelper import generate_preprocessor_outputs, \
    PreprocessorHelper

parametrize = pytest.mark.parametrize
generate_outputs = tests.generateOutputsDecorator.generate_outputs

files_to_test = [
    'includeFishHook.c',
    'includePrecedingWhitespace.c',
    'lessThanInclude.c',
    'nestedInclude.c',
    'oneInclude.c'
]


@generate_outputs
def generate_ast_outputs():
    """Generate the output for the tests.

    """
    folder = dirname(__file__)
    option_arg = '-Itests/preprocessor/include/input'
    generate_preprocessor_outputs(files_to_test, folder, option_arg)


class TestInclude(PreprocessorHelper):

    @parametrize('file_to_test', files_to_test)
    def test_include(self, file_to_test, capsys):
        """Execute the include test.

        Args:
            file_to_test (str): the file to test
            capsys (method): the capsys fixture from pytest
        """
        path_of_this_file = abspath(dirname(__file__))
        include_dirs = ['-Itests/preprocessor/include/input']
        self.execute_test(file_to_test,capsys, path_of_this_file, include_dirs)
