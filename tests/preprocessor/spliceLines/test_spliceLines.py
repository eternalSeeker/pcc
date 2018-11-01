# -*- coding: utf-8 -*-

from pcc.main import main
from os.path import join, abspath, dirname

# The parametrize function is generated, so this doesn't work:
#
#     from pytest.mark import parametrize
#
import pytest
parametrize = pytest.mark.parametrize

files_to_test = [
    'linesplicing_1.c'
]


class TestLineSplicing(object):

    @parametrize('file_to_test', files_to_test)
    def test_lineSplicing(self, file_to_test, capsys):
        inputPath = 'input'
        outputPath = 'output'
        pathOfThisFile = abspath(dirname(__file__))
        inputPath = join(pathOfThisFile, inputPath)
        outputPath = join(pathOfThisFile, outputPath)
        fileToPreprocess = file_to_test
        inputFileWithPath = join(inputPath, fileToPreprocess)
        outputFileWithPath = join(outputPath, fileToPreprocess)
        # this test will not raise SystemExit
        main(['progname', '-E', inputFileWithPath])
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
            'for file %s, size %d != %d, output \n<%s>\n testOut \n<%s>' \
            % (fileToPreprocess, outputListSize, outputFileAsListSize, out,
               outputFileAsString)
        for i in range(outputFileAsListSize):
            assert outputList[i] == outputFileAsList[i], 'for line %d' % i
        # there should be no error
        assert err == ''
