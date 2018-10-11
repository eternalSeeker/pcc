#!/usr/bin/env python3
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

    @staticmethod
    def stringToListWithNewLines(sourceFile):
        list = sourceFile.split('\n')
        for i in range(len(list) - 1):
            list[i] += '\n'
        return list

    @staticmethod
    def assertEqual(a, b):
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
        while backslashAndNewline in self.listOfCodeLines[self.lineCount]:

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
            matchObjQuotes = re.match(r'\s*?#include.*?\"(.*)\".*?',
                                      self.listOfCodeLines[self.lineCount],
                                      re.M | re.I | re.MULTILINE | re.DOTALL)
            matchObjLessThan = re.match(r'\s*?#include.*?<(.*)>.*?',
                                        self.listOfCodeLines[self.lineCount],
                                        re.M | re.I | re.MULTILINE | re.DOTALL)
            if matchObjQuotes:
                self.fillInInclude(matchObjQuotes)
            elif matchObjLessThan:
                self.fillInInclude(matchObjLessThan)
            else:
                # no match, nothing to do
                self.preproccessorWarning('could not parse include statement')
                pass

    def fillInInclude(self, matchObj):
        # there is an include in the file
        # get the filename from the match
        filename = matchObj.group(1)
        # add the current directory to the include dirs
        dirsToSearch = list(os.getcwd())
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
                                    filename)

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
                                            tokenToRemove)
        return linePopped

    def macroDefinitionAndExpansion(self):
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

    def isConditionalCompilationLine(self):
        conditionalCompilationLines = ['#ifdef', '#ifndef', '#if ']
        for lineToExplude in conditionalCompilationLines:
            if lineToExplude in self.listOfCodeLines[self.lineCount]:
                return True
        return False

    def replaceTokens(self):
        # replace all tokens by their token sequence
        areThereTokensLeftInTheLine = True
        while areThereTokensLeftInTheLine and not \
                self.isConditionalCompilationLine():
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
                        argumentList = list(extractedString)
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

    def evaluateContantExpression(self, constantExpression):
        return False

    def conditionCompilation(self):
        if '#if' in self.listOfCodeLines[self.lineCount]:
            ifLine = self.listOfCodeLines[self.lineCount]
            partIsActive = self.checkIfBranchIsActive(ifLine)
            finished = False
            numberOfNestedConditions = 0
            currentIndex = self.lineCount+1
            # add an empty line instead of the #if line
            codeToInclude = ['\n']
            while finished is False \
                    and currentIndex < len(self.listOfCodeLines):
                if '#endif' in self.listOfCodeLines[currentIndex]:
                    finished, numberOfNestedConditions, addLine = \
                        self.processEndif(finished, numberOfNestedConditions)

                elif '#if' in self.listOfCodeLines[currentIndex]:
                    numberOfNestedConditions += 1
                    addLine = True
                elif numberOfNestedConditions > 0:
                    # add all in the nested part
                    addLine = True
                elif '#elif' in self.listOfCodeLines[currentIndex]:
                    # if the part was active, add it
                    # if the part was not active and  became active, do not
                    #   add it
                    # else it was not active so not add it
                    addLine = partIsActive
                    partIsActive = self.checkIfElifIsActive(ifLine,
                                                            partIsActive)
                elif '#else' in self.listOfCodeLines[currentIndex]:
                    # if the part was active, add it
                    # if the part was not active and  became active, do not
                    #   add it
                    # else it was not active so not add it
                    addLine = partIsActive
                    partIsActive = self.isElsePartActive(partIsActive)
                else:
                    addLine = True

                if addLine is True:
                    self.parseLine(codeToInclude, currentIndex, partIsActive)

                currentIndex += 1
            if finished is False:
                message = 'could not find closing #endif'
                self.preproccessorError(message)
            del self.listOfCodeLines[self.lineCount: currentIndex]
            self.listOfCodeLines[self.lineCount:self.lineCount] = \
                codeToInclude

    @staticmethod
    def processEndif(finished, numberOfNestedConditions):
        if numberOfNestedConditions == 0:
            finished = True
        else:
            numberOfNestedConditions -= 1
        if finished is True:
            addLine = False
        else:
            addLine = True
        return finished, numberOfNestedConditions, addLine

    def parseLine(self, codeToInclude, currentIndex, partIsActive):
        if partIsActive is True:
            codeToInclude. \
                append(self.listOfCodeLines[currentIndex])
        else:
            pass

    @staticmethod
    def isElsePartActive(partIsActive):
        if partIsActive is False:
            partIsActive = True
        elif partIsActive is True:
            partIsActive = None
        return partIsActive

    def checkIfElifIsActive(self, ifLine, partIsActive):
        if partIsActive is True:
            partIsActive = None
        elif partIsActive is False:
            constantExpression = ifLine.split('#elif ')[1]
            partIsActive = \
                self.evaluateContantExpression(constantExpression)
        return partIsActive

    def checkIfBranchIsActive(self, ifLine):
        # check the branches of the conditional compilation
        # partIsActive is True if the branch is active
        #                 False if the active branch is not yet encountered
        #                 None if the active branch is already added
        if '#ifdef' in ifLine:
            identifier = ifLine.split('#ifdef')[1]
            identifier = ''.join(identifier.split())

            if identifier in self.tokens.keys():
                partIsActive = True
            else:
                partIsActive = False
        elif '#ifndef' in ifLine:
            identifier = ifLine.split('#ifndef')[1]
            identifier = ''.join(identifier.split())
            if identifier not in self.tokens.keys():
                partIsActive = True
            else:
                partIsActive = False

        else:
            constantExpression = ifLine.split('#if ')[1]
            partIsActive = \
                self.evaluateContantExpression(constantExpression)
        return partIsActive

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
            # K&R A 12.5
            self.conditionCompilation()
            # K&R A 12.7
            self.errorGeneration()
            self.lineCount += 1
            self.souceLineCount += 1

        self.processedFile = ''.join(self.listOfCodeLines)
