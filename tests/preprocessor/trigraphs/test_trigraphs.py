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


class TestTrigraphs(object):

    @parametrize('file_to_test', files_to_test)
    def test_trigraphs(self, file_to_test, capsys):
        inputPath = 'input'
        outputPath = 'output'
        includeDirs = ['-Itests/preprocessor/trigraphs/input']
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
            'for file %s, size %d != %d, output \n<%s>\n testOut \n<%s>' \
            % (fileToPreprocess, outputListSize, outputFileAsListSize,
               out, outputFileAsString)
        for i in range(outputFileAsListSize):
            assert outputList[i] == outputFileAsList[i],  \
                'for file %s, line %d  <%s> != <%s> ' % \
                (fileToPreprocess, i,  outputFileAsList[i], outputList[i])
        # there should be no error
        assert err == ''
