# -*- coding: utf-8 -*-

from pcc.main import main
from os import listdir
from os.path import isfile, join, abspath, dirname

# The parametrize function is generated, so this doesn't work:
#
#     from pytest.mark import parametrize
#
import pytest
parametrize = pytest.mark.parametrize


class TestConditionalCompilation(object):

    @parametrize('preprocessorArg', ['-E'])
    def test_include(self, preprocessorArg, capsys):
        includeDirs = ['-Itests/preprocessor/conditionalCompilation/input']
        inputPath = 'input'
        outputPath = 'output'
        pathOfThisFile = abspath(dirname(__file__))
        inputPath = join(pathOfThisFile, inputPath)
        outputPath = join(pathOfThisFile, outputPath)
        inputFiles = [f for f in listdir(inputPath)
                      if isfile(join(inputPath, f)) and f.endswith(".c")]
        for fileToPreprocess in inputFiles:
            inputFileWithPath = join(inputPath, fileToPreprocess)
            outputFileWithPath = join(outputPath, fileToPreprocess)
            # this test will not raise SystemExit
            argsv = list(['progname'])
            argsv.append(preprocessorArg)
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
                    'for file %s line %d, <%s> != <%s>' %\
                    (fileToPreprocess, i, outputList[i], outputFileAsList[i])
            # there should be no error
            assert err == ''
