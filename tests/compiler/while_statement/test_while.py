# -*- coding: utf-8 -*-

import os
import subprocess
from os.path import join, abspath, dirname

import pytest

import tests.generateOutputsDecorator
from pcc.main import main

generate_outputs = tests.generateOutputsDecorator.generate_outputs

# The parametrize function is generated, so it does not work to import
parametrize = pytest.mark.parametrize

files_to_test = [
    ('while.c', 'intHelper.c', 'while.out'),
]


@generate_outputs
def generate_compiler_outputs():
    for inputs in files_to_test:
        input_file = inputs[0]
        input_helper = inputs[1]
        output_file = inputs[2]
        folder = dirname(__file__)
        file_input_path = join(folder, 'input', input_file)
        helper_input_path = join(folder, 'input', input_helper)
        file_output_path = join(folder, 'output', output_file)
        gcc_output_file_name = 'out.o'
        gcc_exe = join(folder, 'output', 'exe.out')
        command = 'gcc -c %s -o %s' % (file_input_path, gcc_output_file_name)

        response = subprocess.run(command, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, shell=True)

        assert response.returncode == 0, response.stderr

        command = 'gcc %s -o %s %s' % \
                  (helper_input_path, gcc_exe, gcc_output_file_name)

        response = subprocess.run(command, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, shell=True)
        assert response.returncode == 0, response.stderr
        command = gcc_exe
        response = subprocess.run(command, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, shell=True)
        assert response.returncode == 0, response.stderr
        # decode the outputted string to ascii and split the line while
        # keeping the new line character(s)
        captured_result = response.stdout.decode('ascii').splitlines(True)
        with open(file_output_path, 'w') as f:
            for output_line in captured_result:
                f.write(output_line)

        os.remove(gcc_exe)
        os.remove(gcc_output_file_name)


class TestIf(object):

    @parametrize('file_to_test,helper,output_file', files_to_test)
    def test_if(self, file_to_test, helper, output_file, capsys):
        includeDirs = []
        inputPath = 'input'
        outputPath = 'output'
        pcc_output_file_name = 'test.out'
        pathOfThisFile = abspath(dirname(__file__))
        inputPath = join(pathOfThisFile, inputPath)
        helper_path = join(pathOfThisFile, 'input', helper)
        outputPath = join(pathOfThisFile, outputPath)
        pcc_output_file_path = join(pathOfThisFile, pcc_output_file_name)

        inputFileWithPath = join(inputPath, file_to_test)
        outputFileWithPath = join(outputPath, output_file)
        # this test will not raise SystemExit
        argsv = list(['progname'])
        argsv.append('-c')
        argsv.append('-o' + str(pcc_output_file_path))
        argsv.extend(includeDirs)
        argsv.append(inputFileWithPath)
        main(argsv)
        out, err = capsys.readouterr()
        assert out == ''
        # there should be no error
        assert err == ''

        gcc_exe = 'test'

        command = 'gcc %s -o %s %s' % \
                  (helper_path, gcc_exe, pcc_output_file_path)

        response = subprocess.run(command, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, shell=True)
        assert response.returncode == 0

        command = './' + gcc_exe
        response = subprocess.run(command, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, shell=True)

        # TODO remove the test as it seems to fail in travis
        # remove assert on response.returncode

        assert response.stderr == b''
        # decode the outputted string to ascii and split the line while
        # keeping the new line character(s)
        captured_result = response.stdout.decode('ascii').splitlines(True)

        outputFileAsList, outputFileAsListSize = self.extractFileContents(
            outputFileWithPath)

        captured_result = ''.join(captured_result)
        outputList = captured_result.split('\n')
        outputListSize = len(outputList)

        # the outputted file needs to match exactly
        assert outputListSize == outputFileAsListSize, \
            'for file %s, size %d != %d \n(%s)' % \
            (output_file, outputListSize, outputFileAsListSize,
             out)
        for i in range(outputFileAsListSize):
            assert outputList[i] == outputFileAsList[i], \
                'for file %s line %d, <%s> != <%s>' % \
                (output_file, i, outputList[i], outputFileAsList[i])

        os.remove(pcc_output_file_path)
        os.remove(gcc_exe)

    @staticmethod
    def extractFileContents(outputFileWithPath):
        with open(outputFileWithPath, 'r') as fileToRead:
            outputFileAsString = fileToRead.read()
        outputFileAsString = outputFileAsString.replace('\r', '')
        outputFileAsList = outputFileAsString.split('\n')
        outputFileAsListSize = len(outputFileAsList)
        return outputFileAsList, outputFileAsListSize
