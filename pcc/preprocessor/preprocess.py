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

    def assertEqual(self, a, b):
        if isinstance(a, str):
            assert a == b, '<%s> != <%s>' % (a, b)
        else:
            assert a == b, '<%s> != <%s>' % (str(a), str(b))

    def replaceSubStringCurrentLine(self, old, new):
        self.listOfCodeLines[self.lineCount] = \
            self.listOfCodeLines[self.lineCount].replace(old, new)

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
            self.replaceSubStringCurrentLine(key, self.trigraphs[key])

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
        while '#define' in self.listOfCodeLines[self.lineCount]:
            matchObj = re.match(r'.*?#define(.*)',
                                self.listOfCodeLines[self.lineCount],
                                re.M | re.I | re.DOTALL)
            if matchObj:
                list = matchObj.group(1).split()
                token = list[0]
                if len(list) > 1:
                    tokenSequence = ''.join(list[1:])
                else:
                    tokenSequence = ''
                self.tokens[token] = tokenSequence
                self.listOfCodeLines.pop(self.lineCount)
            else:
                self.dumpCodeList()
        # replace all tokens by their token sequence
        areThereTokensLeftInTheLine = True
        while areThereTokensLeftInTheLine:
            areThereTokensLeftInTheLine = False
            for token in self.tokens.keys():
                if token in self.listOfCodeLines[self.lineCount]:
                    self.replaceSubStringCurrentLine(token, self.tokens[token])
                    areThereTokensLeftInTheLine = True

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
            self.macroDefinitionAndExpansion()
            # R&R A 12.4
            self.includeFiles()
            self.lineCount += 1

        self.processedFile = ''.join(self.listOfCodeLines)
