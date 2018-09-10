#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import re
import os.path
import pprint
import pcc.utils.warning
import pcc.utils.stringParsing


class MacroObject:

    def __init__(self, identifier, argumentList, tokenSequence):
        self.identifier = identifier
        self.tokenSequence = tokenSequence
        self.argumentList = argumentList

    def getNumberOfArguments(self):
        return len(self.argumentList)

    def getIdentifier(self):
        return self.identifier

    def getTokenSequence(self):
        return self.tokenSequence

    def fillInMacro(self, arguments):
        macroString = self.tokenSequence
        assert len(self.argumentList) == 2, '%d' % len(self.argumentList)
        for i in range(len(self.argumentList)):
            macroString = macroString.replace(self.argumentList[i],
                                              arguments[i])

        return macroString


class Preprocessor:

    def preproccessorWarning(self, message):
        pcc.utils.warning.warning(self.originalInputFileName,
                                  self.souceLineCount, message)

    def preproccessorError(self, message):
        pcc.utils.warning.error(self.originalInputFileName,
                                self.souceLineCount, message)

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

    def __init__(self, inputFile, inputFileAsString, includeDirs):
        self.originalInputFileName = inputFile
        self.originalInputFile = copy.copy(inputFileAsString)
        self.processedFile = ''
        self.tokens = dict()
        self.includeDirs = includeDirs
        self.listOfCodeLines = []
        self.lineCount = 0
        self.souceLineCount = 1
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
            self.souceLineCount += 1

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
                self.preproccessorWarning('could not parse include statement')
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
            self.preproccessorError('file to include <%s> not found' %
                                    (filename))

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

    def removeTokens(self):
        linePopped = False
        if '#undef' in self.listOfCodeLines[self.lineCount]:
            matchObj = re.match(r'.*?#undef (.*)',
                                self.listOfCodeLines[self.lineCount],
                                re.M | re.I | re.DOTALL)
            if matchObj:
                # remove all spaces and only look at the first element
                tokenToRemove = matchObj.group(1).split()[0]
                if tokenToRemove in self.tokens.keys():
                    self.tokens.pop(tokenToRemove, None)
                    self.listOfCodeLines.pop(self.lineCount)
                    self.souceLineCount += 1
                    linePopped = True
                else:
                    self.preproccessorError('token <%s> does not exist' %
                                            (tokenToRemove))
        return linePopped

    def macroDefinitionAndExpansion(self):
        linePopped = False
        # loop until there are no more lines removed from the list
        while True:
            linePopped = self.addTokens()
            if linePopped is True:
                continue
            linePopped = self.removeTokens()
            if linePopped is True:
                continue
            self.replaceTokens()
            break

    def replaceTokens(self):
        # replace all tokens by their token sequence
        areThereTokensLeftInTheLine = True
        while areThereTokensLeftInTheLine:
            areThereTokensLeftInTheLine = False
            for token in self.tokens.keys():
                areThereTokensLeftInTheLine = self.replaceTokenIfFound(
                    areThereTokensLeftInTheLine, token)

    def replaceTokenIfFound(self, areThereTokensLeftInTheLine, token):
        if token in self.listOfCodeLines[self.lineCount]:
            obj = self.tokens[token]
            if obj.getNumberOfArguments() == 0:
                self.\
                    replaceSubStringCurrentLine(token, obj.getTokenSequence())
            else:
                startIndex = self.listOfCodeLines[self.lineCount]. \
                    find(token)
                argumentString = pcc.utils.stringParsing.\
                    extractTextForEnclosedParenthesis(self.listOfCodeLines[
                                                      self.lineCount],
                                                      startIndex)
                if argumentString.count(',') > 0:
                    args = argumentString.split(',')
                else:
                    args = list(argumentString)
                macroString = obj.fillInMacro(args)
                stringToReplace = token + '(' + argumentString + ')'
                self.replaceSubStringCurrentLine(stringToReplace,
                                                 macroString)
            areThereTokensLeftInTheLine = True
        return areThereTokensLeftInTheLine

    def addTokens(self):
        linePopped = False
        while '#define' in self.listOfCodeLines[self.lineCount]:
            matchObj = re.match(r'.*?#define (.*)',
                                self.listOfCodeLines[self.lineCount],
                                re.M | re.I | re.DOTALL)
            if matchObj:
                list = matchObj.group(1).split()
                token = list[0]
                if '(' in token:
                    startIndex = 0
                    extractedString = pcc.utils.stringParsing.\
                        extractTextForEnclosedParenthesis(token, startIndex)
                    numberOfArguments = extractedString.count(',') + 1
                    if numberOfArguments >= 1:
                        argumentList = extractedString.split(',')
                    else:
                        argumentList = []
                        argumentList.append(extractedString)
                    identifier = token.split('(')[0]
                else:
                    identifier = token
                    argumentList = []

                if len(list) > 1:
                    tokenSequence = ''.join(list[1:])
                else:
                    tokenSequence = ''
                obj = MacroObject(identifier, argumentList, tokenSequence)
                if identifier in self.tokens.keys():
                    self.preproccessorError('Macro already defined')
                else:
                    self.tokens[identifier] = obj
                self.listOfCodeLines.pop(self.lineCount)
                self.souceLineCount += 1
                linePopped = True
            else:
                self.dumpCodeList()
        return linePopped

    def errorGeneration(self):
        if '#error' in self.listOfCodeLines[self.lineCount]:

            matchObj = re.match(r'.*?#error(.*)',
                                self.listOfCodeLines[self.lineCount],
                                re.M | re.I | re.DOTALL)
            if matchObj:
                message = ''
                if matchObj.group(1):
                    message = matchObj.group(1)
                self.preproccessorError(message)
                self.listOfCodeLines.pop(self.lineCount)
                self.souceLineCount += 1

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
        self.souceLineCount = 1
        while self.lineCount < len(self.listOfCodeLines):
            # K&R A 12.1
            self.runTrigraphReplacement()
            self.lineCount += 1
            self.souceLineCount += 1

        self.lineCount = 0
        self.souceLineCount = 1
        while self.lineCount < len(self.listOfCodeLines):
            # K&R A 12.2
            self.lineSplicing()
            self.lineCount += 1
            self.souceLineCount += 1

        self.lineCount = 0
        self.souceLineCount = 1
        while self.lineCount < len(self.listOfCodeLines):
            # K&R A 12.3
            self.macroDefinitionAndExpansion()
            # K&R A 12.4
            self.includeFiles()

            # K&R A 12.7
            self.errorGeneration()
            self.lineCount += 1
            self.souceLineCount += 1

        self.processedFile = ''.join(self.listOfCodeLines)
