# -*- coding: utf-8 -*-

import subprocess
from os.path import join, abspath, dirname

# The parametrize function is generated, so it does not work to import
import pytest

import tests.generateOutputsDecorator
from pcc.main import main

parametrize = pytest.mark.parametrize
generate_outputs = tests.generateOutputsDecorator.generate_outputs

files_to_test = [
    'error.c',
    'error_noMessage.c'
]


@generate_outputs
def generate_ast_outputs():
    for file in files_to_test:
        folder = dirname(__file__)
        file_input_path = join(folder, 'input', file)
        file_output_path = join(folder, 'output', file)
        command = 'gcc -E %s' % file_input_path

        response = subprocess.run(command, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, shell=True)
        # decode the outputted string to ascii and split the line while
        # keeping the new line character(s)
        captured_result = response.stderr.decode('ascii').splitlines(True)
        captured_result = captured_result[1]
        if response:
            if response.returncode != 0:
                with open(file_output_path, 'w') as f:
                    for output_line in captured_result:
                        if '#' not in output_line:
                            f.write(output_line)
            else:
                print('ERROR checking %s, got <%s>' % (file, response.stderr))


class TestErrorGeneration(object):

    @parametrize('file_to_test', files_to_test)
    def test_include(self, file_to_test, capsys):
        include_dirs = ['-Itests/preprocessor/include/input']
        input_path = 'input'
        path_of_this_file = abspath(dirname(__file__))
        input_path = join(path_of_this_file, input_path)
        file_to_preprocess = file_to_test
        input_file_with_path = join(input_path, file_to_preprocess)

        # this test will not raise SystemExit
        argsv = list(['progname'])
        argsv.append('-E')
        argsv.extend(include_dirs)
        argsv.append(input_file_with_path)
        main(argsv)
        out, err = capsys.readouterr()

        # there should be an error
        assert err is not None
        assert "ERROR:" in err
        assert "file " in err
        assert "line " in err
