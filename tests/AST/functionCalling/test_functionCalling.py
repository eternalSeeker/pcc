# -*- coding: utf-8 -*-

from pcc.main import main
from os.path import join, abspath, dirname
import pycparser
import tests.generateOutputsDecorator
import pytest


generate_outputs = tests.generateOutputsDecorator.generate_outputs

# The parametrize function is generated, so this doesn't work:
#
#     from pytest.mark import parametrize
#

parametrize = pytest.mark.parametrize

files_to_test = [
    'simple.c'
]


@generate_outputs
def generate_ast_outputs():
    for file in files_to_test:
        folder = dirname(__file__)
        file_input_path = join(folder, 'input', file)
        file_output_path = join(folder, 'output', file)

        output_buffer = open(file_output_path, 'w')
        ast = pycparser.parse_file(file_input_path, use_cpp=False)
        ast.show(buf=output_buffer, showcoord=False)
        output_buffer.close()


class TestFunctionCalling(object):

    @parametrize('file_to_test', files_to_test)
    def test_functionCalling(self, file_to_test, capsys):
        includeDirs = []
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
        argsv.append('-fdump_tree')
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
            'for file %s, size %d != %d \n(%s)' % \
            (fileToPreprocess, outputListSize, outputFileAsListSize,
             out)
        for i in range(outputListSize):
            assert outputList[i] == outputFileAsList[i], \
                'for file %s line %d, <%s> != <%s>' %\
                (fileToPreprocess, i, outputList[i], outputFileAsList[i])
        # there should be no error
        assert err == ''
