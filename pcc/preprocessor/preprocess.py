#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import re
import os.path
import pprint


class Preprocessor:

    def stringToListWithNewLines(self, sourceFile):
        list = sourceFile.split('\n')
        for i in range(len(list) - 1):
            list[i] += '\n'
        return list

    def __init__(self, inputFileAsString, includeDirs):
        self.originalInputFile = copy.copy(inputFileAsString)
        self.processedFile = ''
        self.tokens = dict()
        self.includeDirs = includeDirs
        self.listOfCodeLines = []
        self.lineCount = 0
        self.trigraphs = {
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
        for key in self.trigraphs.keys():
            tmp = self.listOfCodeLines[self.lineCount].\
                replace(key, self.trigraphs[key])
            self.listOfCodeLines[self.lineCount] = tmp

    def lineSplicing(self):
        backslashAndNewline = '\\\n'
        while(backslashAndNewline in self.listOfCodeLines[self.lineCount]):

            tmp = self.listOfCodeLines[self.lineCount].\
                replace(backslashAndNewline, '')

            self.listOfCodeLines[self.lineCount] = \
                tmp + self.listOfCodeLines[self.lineCount + 1]
            self.listOfCodeLines.pop(self.lineCount + 1)

    def includeFiles(self):
        if '#include' in self.listOfCodeLines[self.lineCount]:
            # regex DOTALL dot also matches newline,
            # .*? any sequence of chars optional
            # TODO #include can only start with whitespace chars
            matchObj = re.match(r'.*?#include.*?\"(.*)\".*?',
                                self.listOfCodeLines[self.lineCount],
                                re.M | re.I | re.MULTILINE | re.DOTALL)
            if matchObj:
                self.fillInInclude(matchObj)
            else:
                # no match, nothing to do
                pass

    def fillInInclude(self, matchObj):
        # there is an include in the file
        # get the filename from the match
        filename = matchObj.group(1)
        dirsToSearch = []
        # add the current dirrectory to the include dirs
        dirsToSearch.append(os.getcwd())
        if self.includeDirs:
            dirsToSearch.extend(self.includeDirs)
        isFileFound = False
        for dir in dirsToSearch:
            fileWithDir = os.path.join(dir, filename)
            if os.path.isfile(fileWithDir):
                # the file to include exists
                with open(fileWithDir, 'r') as fileToInclude:
                    self.replaceIncludeWithContentOfFile(fileToInclude)
                    isFileFound = True
        if isFileFound is False:
            # error file does not exist
            # TODO issue an error if the file does not exits
            assert filename is None
            assert filename is not None
            pass

    def replaceIncludeWithContentOfFile(self, fileToInclude):
        includedFile = fileToInclude.read()
        includedFile = includedFile.replace('\r', '')
        includedFileAsList = \
            self.stringToListWithNewLines(includedFile)
        includedFileAsList[-1] += '\n'
        self.listOfCodeLines.pop(self.lineCount)
        self.listOfCodeLines[self.lineCount:self.lineCount] = \
            includedFileAsList

    def dumpCodeList(self):
        assert self.listOfCodeLines is None, '<%s>' % (
            pprint.pprint(self.listOfCodeLines))

    def macroDefinitionAndExpansion(self):
        if '#define' in self.listOfCodeLines[self.lineCount]:
            matchObj = re.match(r'.*?#define(.*)\s*(.*)',
                                self.listOfCodeLines[self.lineCount],
                                re.M | re.I | re.DOTALL)
            if matchObj:
                token = matchObj.group(1)
                tokenSequence = matchObj.group(2)
                assert token == '', 'token <%s>' % (token)
                self.tokens[token] = tokenSequence
                self.listOfCodeLines[self.lineCount] = \
                    re.sub(r'\s*?#define'+token+'.*?\n', ' ',
                           self.listOfCodeLines[self.lineCount],
                           re.M | re.I | re.MULTILINE | re.DOTALL)
            else:
                pass
                # assert self.listOfCodeLines[self.lineCount] == '', \
                #    'file <%s>' % ( self.listOfCodeLines[self.lineCount] )

    def preprocess(self):
        # restart the preprocessing from the original file
        sourceFile = copy.copy(self.originalInputFile)
        # Remove all carriage returns if present in the file
        sourceFile = sourceFile.replace('\r', '')
        # split the source file in lines of code
        # but do not remove the '\n' char
        list = self.stringToListWithNewLines(sourceFile)
        self.listOfCodeLines = copy.copy(list)

        self.lineCount = 0
        while self.lineCount < len(self.listOfCodeLines):
            # K&R A 12.1
            self.runTrigraphReplacement()
            self.lineCount += 1

        self.lineCount = 0
        while self.lineCount < len(self.listOfCodeLines):
            # K&R A 12.2
            self.lineSplicing()
            self.lineCount += 1

        self.lineCount = 0
        while self.lineCount < len(self.listOfCodeLines):
            # K&R A 12.3
            # self.macroDefinitionAndExpansion()
            # R&R A 12.4
            self.includeFiles()
            self.lineCount += 1
        self.processedFile = ''.join(self.listOfCodeLines)
