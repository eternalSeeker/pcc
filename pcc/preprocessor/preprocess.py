#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import re
import os.path


class Preprocessor:

    def __init__(self, inputFileAsString):
        self.originalInputFile = copy.copy(inputFileAsString)
        self.processedFile = ''
        Preprocessor.trigraphs = {
            '??=':  '#',
            '??/':  '\\',
            '??\'': '^',
            '??(':  '[',
            '??)':  ']',
            '??!':  '|',
            '??<':  '{',
            '??>':  '}',
            '??-':  '~'
        }

    def runTrigraphReplacement(self):
        for key in Preprocessor.trigraphs.keys():
            self.processedFile = self.processedFile.replace(
                key, Preprocessor.trigraphs[key])

    def lineSplicing(self):
        backslashAndNewline = '\\\n'
        self.processedFile = self.processedFile.replace(
            backslashAndNewline, '')

    def includeFiles(self):
        patternStart = '#include \"'
        patternEnd = '\"'
        pattern = patternStart + '(.*)' + patternEnd
        result = re.match(pattern, self.processedFile)
        if result:
            # there is an include in the file
            # get the filename from the match
            filename = result.group(1)
            if os.path.isfile(filename):
                # the file to include exists
                with open(filename, 'r') as fileToInclude:
                    includedFile = fileToInclude.read()
                    stringToReplace = patternStart + filename + patternEnd
                    self.processedFile = self.processedFile.replace(
                        stringToReplace, includedFile)
            else:
                # error file does not exist
                # TODO issue an error if the file does not exits
                pass
        else:
            # no match, nothing to do
            pass

    def preprocess(self):
        # restart the preprocessing from the original file
        self.processedFile = copy.copy(self.originalInputFile)
        # R&R A 12.1
        self.runTrigraphReplacement()
        # R&R A 12.2
        self.lineSplicing()

        # R&R A 12.4
        self.includeFiles()
