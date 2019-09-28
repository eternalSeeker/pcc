# -*- coding: utf-8 -*-

# The parametrize function is generated, so it does not work to import
import re
import subprocess
from os.path import join, abspath, dirname

import pytest

import tests.generateOutputsDecorator
from tests.preprocessor.preprocessorhelper import PreprocessorHelper

parametrize = pytest.mark.parametrize
generate_outputs = tests.generateOutputsDecorator.generate_outputs

files_to_test = [
    'allSigns.c',
    'caretSign.c',
    'closeBracketSign.c',
    'openBraceSign.c',
    'pipeSign.c',
    'tildeSign.c',
    'backslashSign.c',
    'closeBraceSign.c',
    'openBracketSign.c',
    'poundSign.c'
]


class TestTrigraphs(PreprocessorHelper):

    @parametrize('file_to_test', files_to_test)
    def test_trigraphs(self, file_to_test, capsys):
        """Execute the trigraphs test.

        Args:
            file_to_test (str): the file to test
            capsys (method): the capsys fixture from pytest
        """
        path_of_this_file = abspath(dirname(__file__))
        include_dirs = ['-Itests/preprocessor/trigraphs/input']
        self.execute_test(file_to_test, capsys, path_of_this_file,
                          include_dirs)


@generate_outputs
def generate_ast_outputs():
    for file in files_to_test:
        folder = dirname(__file__)
        file_input_path = join(folder, 'input', file)
        file_output_path = join(folder, 'output', file)
        command = 'gcc -trigraphs -E %s' % file_input_path

        response = subprocess.run(command, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, shell=True)
        # decode the outputted string to ascii and split the line while
        # keeping the new line character(s)
        captured_result = response.stdout.decode('ascii').splitlines(True)

        if response:
            if response.returncode == 0:
                with open(file_output_path, 'w') as f:
                    for output_line in captured_result:
                        match = re.match(r'# \d+ ', output_line, flags=0)
                        if match is None:
                            f.write(output_line)
            else:
                print('ERROR checking %s, got <%s>' % (file, response.stderr))
