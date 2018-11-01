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
    'error.c',
    'error_noMessage.c'
]


class TestErrorGeneration(object):

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

        # there should be an error
        assert err is not None
        assert "ERROR:" in err
        assert "file " in err
        assert "line " in err

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
