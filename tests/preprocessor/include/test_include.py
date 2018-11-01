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
    'includeFishHook.c',
    'includePrecedingWhitespace.c',
    'lessThanInclude.c',
    'nestedInclude.c',
    'oneInclude.c'
]


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
