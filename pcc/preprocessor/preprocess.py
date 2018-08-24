#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import re
import os.path


class Preprocessor:

    def __init__(self, inputFileAsString, includeDirs):
        self.originalInputFile = copy.copy(inputFileAsString)
        self.processedFile = ''
        self.includeDirs = includeDirs
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
        while '#include' in self.processedFile:
            # regex DOTALL dot also matches newline,
            # .*? any sequence of chars optional
            # TODO #include can only start with whitespace chars
            matchObj = re.match(r'.*?#include.*?\"(.*)\".*?',
                                self.processedFile,
                                re.M | re.I | re.MULTILINE | re.DOTALL)
            if matchObj:
                # there is an include in the file
                # get the filename from the match
                filename = matchObj.group(1)

                dirsToSearch = []
                dirsToSearch.append(os.getcwd())
                if self.includeDirs:
                    dirsToSearch.extend(self.includeDirs)
                isFileFound = False
                for dir in dirsToSearch:
                    fileWithDir = os.path.join(dir, filename)
                    if os.path.isfile(fileWithDir):
                        # the file to include exists
                        with open(fileWithDir, 'r') as fileToInclude:
                            includedFile = fileToInclude.read()
                            includedFile = includedFile.replace('\r', '')
                            self.processedFile = \
                                re.sub(r'.*?#include.*?\"'
                                       + filename + '\".*?',
                                       includedFile, self.processedFile,
                                       re.M | re.I | re.MULTILINE | re.DOTALL)
                            isFileFound = True

                if isFileFound is False:
                    # error file does not exist
                    # TODO issue an error if the file does not exits
                    assert filename is None
                    assert filename is not None
                    pass
            else:
                # no match, nothing to do
                pass

    def preprocess(self):
        # restart the preprocessing from the original file
        self.processedFile = copy.copy(self.originalInputFile)
        # Remove all carriage returns if present in the file
        self.processedFile = self.processedFile.replace('\r', '')
        # R&R A 12.1
        self.runTrigraphReplacement()
        # R&R A 12.2
        self.lineSplicing()

        # R&R A 12.4
        self.includeFiles()
