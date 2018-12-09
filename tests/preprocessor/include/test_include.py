# -*- coding: utf-8 -*-

from pcc.main import main
from os.path import join, abspath, dirname

# The parametrize function is generated, so this doesn't work:
#
#     from pytest.mark import parametrize
#
import pytest
import subprocess
import tests.generateOutputsDecorator
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
    for file in files_to_test:
        folder = dirname(__file__)
        file_input_path = join(folder, 'input', file)
        file_output_path = join(folder, 'output', file)
        command = 'gcc -E -Itests/preprocessor/include/input %s' % \
                  file_input_path

        response = subprocess.run(command, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, shell=True)
        # decode the outputted string to ascii and split the line while
        # keeping the new line character(s)
        captured_result = response.stdout.decode('ascii').splitlines(True)

        if response:
            if response.returncode == 0:
                with open(file_output_path, 'w') as f:
                    for output_line in captured_result:
                        if '#' not in output_line:
                            f.write(output_line)
            else:
                print('ERROR checking %s, got <%s>' % (file, response.stderr))


class TestInclude(object):

    @parametrize('file_to_test', files_to_test)
    def test_include(self, file_to_test, capsys):
        includeDirs = ['-Itests/preprocessor/include/input']
        inputPath = 'input'
        outputPath = 'output'
        pathOfThisFile = abspath(dirname(__file__))
        inputPath = join(pathOfThisFile, inputPath)
        outputPath = join(pathOfThisFile, outputPath)
        fileToPreprocess = file_to_test
        inputFileWithPath = join(inputPath, fileToPreprocess)
        outputFileWithPath = join(outputPath, fileToPreprocess)
        # this test will not raise SystemExit
        argsv = list(['progname'])
        argsv.append('-E')
        argsv.extend(includeDirs)
        argsv.append(inputFileWithPath)
        main(argsv)
        out, err = capsys.readouterr()
        with open(outputFileWithPath, 'r') as fileToRead:
            outputFileAsString = fileToRead.read()
        # the outputted file needs to match exactly
        outputFileAsString = outputFileAsString.replace('\r', '')
        outputList = out.split('\n')
        outputFileAsList = outputFileAsString.split('\n')
        outputListSize = len(outputList)
        outputFileAsListSize = len(outputFileAsList)
        assert outputListSize == outputFileAsListSize, \
            'for file %s, size %d != %d' % \
            (fileToPreprocess, outputListSize, outputFileAsListSize)
        for i in range(outputFileAsListSize):
            assert outputList[i] == outputFileAsList[i], \
                'for line %d, <%s> != <%s>' %\
                (i, outputList[i], outputFileAsList[i])
        # there should be no error
        assert err == ''
