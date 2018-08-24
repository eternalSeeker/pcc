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


class TestLineSplicing(object):

    @parametrize('preprocessorArg', ['-E'])
    def test_lineSplicing(self, preprocessorArg, capsys):
        inputPath = 'input'
        outputPath = 'output'
        pathOfThisFile = abspath(dirname(__file__))
        inputPath = join(pathOfThisFile, inputPath)
        outputPath = join(pathOfThisFile, outputPath)
        inputFiles = [f for f in listdir(inputPath)
                      if isfile(join(inputPath, f))]
        for fileToPreprocess in inputFiles:
            inputFileWithPath = join(inputPath, fileToPreprocess)
            outputFileWithPath = join(outputPath, fileToPreprocess)
            # this test will not raise SystemExit
            main(['progname', preprocessorArg, inputFileWithPath])
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
                assert outputList[i] == outputFileAsList[i], 'for line %d' % i
            # there should be no error
            assert err == ''
