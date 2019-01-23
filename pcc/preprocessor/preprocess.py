#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import re
import os.path
import pprint
import pcc.utils.warning
import pcc.utils.stringParsing
from .constantExpression import constantExpression


class MacroObject:

    def __init__(self, identifier, argument_list, token_sequence):
        self.identifier = identifier
        self.tokenSequence = token_sequence
        self.argumentList = argument_list

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
                                  self.sourceLineCount, message)

    def preproccessorError(self, message):
        pcc.utils.warning.error(self.originalInputFileName,
                                self.sourceLineCount, message)

    @staticmethod
    def stringToListWithNewLines(source_file):
        source_file_list = source_file.split('\n')
        for i in range(len(source_file_list) - 1):
            source_file_list[i] += '\n'
        return source_file_list

    @staticmethod
    def assertEqual(a, b):
        if isinstance(a, str):
            assert a == b, '<%s> != <%s>' % (a, b)
        else:
            assert a == b, '<%s> != <%s>' % (str(a), str(b))

    def replaceSubStringCurrentLine(self, old, new):
        self.listOfCodeLines[self.lineCount] = \
            self.listOfCodeLines[self.lineCount].replace(old, new)

    def __init__(self, input_file, input_file_string, include_dirs):
        self.originalInputFileName = input_file
        self.originalInputFile = copy.copy(input_file_string)
        self.processedFile = ''
        self.tokens = dict()
        self.includeDirs = include_dirs
        self.listOfCodeLines = []
        self.lineCount = 0
        self.sourceLineCount = 1
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
            self.listOfCodeLines[self.lineCount + 1] = '\n'
            self.sourceLineCount += 1

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

    def fillInInclude(self, match_obj):
        # there is an include in the file
        # get the filename from the match
        filename = match_obj.group(1)
        # add the current directory to the include dirs
        dirsToSearch = list(os.getcwd())
        if self.includeDirs:
            dirsToSearch.extend(self.includeDirs)
        isFileFound = False
        for dir_to_search in dirsToSearch:
            fileWithDir = os.path.join(dir_to_search, filename)
            if os.path.isfile(fileWithDir):
                # the file to include exists
                with open(fileWithDir, 'r') as fileToInclude:
                    self.replaceIncludeWithContentOfFile(fileToInclude)
                    isFileFound = True
        if isFileFound is False:
            # error file does not exist
            self.preproccessorError('file to include <%s> not found' %
                                    filename)

    def replaceIncludeWithContentOfFile(self, file_to_include):
        includedFile = file_to_include.read()
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
                    # remove the line of the undef statement
                    self.listOfCodeLines[self.lineCount] = '\n'
                    self.sourceLineCount += 1
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
        for lineToExclude in conditionalCompilationLines:
            if lineToExclude in self.listOfCodeLines[self.lineCount]:
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

    def replaceTokenIfFound(self, are_there_tokens_left_in_the_line, token):
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
            are_there_tokens_left_in_the_line = True
        return are_there_tokens_left_in_the_line

    def addTokens(self):
        linePopped = False
        while '#define' in self.listOfCodeLines[self.lineCount]:
            matchObj = re.match(r'.*?#define (.*)',
                                self.listOfCodeLines[self.lineCount],
                                re.M | re.I | re.DOTALL)
            if matchObj:
                list_of_tokens = matchObj.group(1).split()
                token = list_of_tokens[0]
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

                if len(list_of_tokens) > 1:
                    # find the start of the sequence part of the Macro,
                    # by finding all occurrences for the substring
                    # 'list_of_tokens[1]' in the complete match object
                    # (this retains spacing information)
                    original_string = matchObj.group(1)
                    start_of_sequence_string = list_of_tokens[1]
                    starts = [match.start() for match in re.finditer(
                        re.escape(start_of_sequence_string), original_string)]
                    start_of_sequence = starts[-1]
                    tokenSequence = original_string[start_of_sequence:]
                    tokenSequence = tokenSequence.replace('\n', '')
                else:
                    tokenSequence = ''
                obj = MacroObject(identifier, argumentList, tokenSequence)
                if identifier in self.tokens.keys():
                    self.preproccessorError('Macro already defined')
                else:
                    self.tokens[identifier] = obj
                # clear the line that contained the define
                self.listOfCodeLines[self.lineCount] = '\n'
                self.sourceLineCount += 1
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
                self.sourceLineCount += 1

    @staticmethod
    def evaluateConstantExpression(expression_string):
        expression = constantExpression(expression_string)
        evaluation = expression.evaluate()
        return evaluation

    def conditionCompilation(self):

        if '#if' in self.listOfCodeLines[self.lineCount]:
            ifLine = self.listOfCodeLines[self.lineCount]
            partIsActive = self.checkIfBranchIsActive(ifLine)
            finished = False
            numberOfNestedConditions = 0
            currentIndex = self.lineCount+1
            # add an empty line instead of the #if line
            codeToInclude = ['\n']
            currentIndex, finished = \
                self.add_active_branch(codeToInclude, currentIndex, finished,
                                       ifLine, numberOfNestedConditions,
                                       partIsActive)
            if finished is False:
                message = 'could not find closing #endif'
                self.preproccessorError(message)

            del self.listOfCodeLines[self.lineCount: currentIndex]
            self.listOfCodeLines[self.lineCount:self.lineCount] = codeToInclude
            assert True

    def add_active_branch(self, code_to_include, current_index, finished,
                          if_line, number_of_nested_conditions,
                          part_is_active):
        while finished is False and current_index < len(self.listOfCodeLines):
            if '#endif' in self.listOfCodeLines[current_index]:
                finished, number_of_nested_conditions = \
                    self.processEndif(finished, number_of_nested_conditions,
                                      current_index)

            elif '#if' in self.listOfCodeLines[current_index]:
                number_of_nested_conditions += 1
            elif number_of_nested_conditions > 0:
                # add all in the nested part
                pass
            elif '#elif' in self.listOfCodeLines[current_index]:
                # if the part was active, add it
                # if the part was not active and  became active, do not
                #   add it
                # else it was not active so not add it
                # TODO not correct
                part_is_active = self.checkIfElifIsActive(if_line,
                                                          part_is_active)
            elif '#else' in self.listOfCodeLines[current_index]:
                # if the part was active, add it
                # if the part was not active and  became active, do not
                #   add it
                # else it was not active so not add it
                part_is_active = self.isElsePartActive(part_is_active)
                self.listOfCodeLines[current_index] = '\n'
            else:
                pass

            self.parseLine(code_to_include, current_index, part_is_active)

            current_index += 1
        return current_index, finished

    def processEndif(self, finished, number_of_nested_conditions,
                     current_index):
        if number_of_nested_conditions == 0:
            finished = True
            self.listOfCodeLines[current_index] = '\n'
        else:
            number_of_nested_conditions -= 1
        return finished, number_of_nested_conditions

    def parseLine(self, code_to_include, current_index, part_is_active):
        if part_is_active is True:
            code_to_include.append(self.listOfCodeLines[current_index])
        else:
            pass

    @staticmethod
    def isElsePartActive(part_is_active):
        if part_is_active is False:
            part_is_active = True
        elif part_is_active is True:
            part_is_active = None
        return part_is_active

    def checkIfElifIsActive(self, if_line, part_is_active):
        if part_is_active is True:
            part_is_active = None
        elif part_is_active is False:
            expression = if_line.split('#elif ')[1]
            part_is_active = self.evaluateConstantExpression(expression)
        return part_is_active

    def checkIfBranchIsActive(self, if_line):
        # check the branches of the conditional compilation
        # partIsActive is True if the branch is active
        #                 False if the active branch is not yet encountered
        #                 None if the active branch is already added
        if '#ifdef' in if_line:
            identifier = if_line.split('#ifdef')[1]
            identifier = ''.join(identifier.split())

            if identifier in self.tokens.keys():
                partIsActive = True
            else:
                partIsActive = False
        elif '#ifndef' in if_line:
            identifier = if_line.split('#ifndef')[1]
            identifier = ''.join(identifier.split())
            if identifier not in self.tokens.keys():
                partIsActive = True
            else:
                partIsActive = False

        else:
            expression = if_line.split('#if ')[1]
            partIsActive = \
                self.evaluateConstantExpression(expression)
        return partIsActive

    def preprocess(self):
        # restart the preprocessing from the original file
        sourceFile = copy.copy(self.originalInputFile)
        # Remove all carriage returns if present in the file
        sourceFile = sourceFile.replace('\r', '')
        # split the source file in lines of code
        # but do not remove the '\n' char
        list_of_code = self.stringToListWithNewLines(sourceFile)
        self.listOfCodeLines = copy.copy(list_of_code)

        self.lineCount = 0
        self.sourceLineCount = 1
        while self.lineCount < len(self.listOfCodeLines):
            # K&R A 12.1
            self.runTrigraphReplacement()
            self.lineCount += 1
            self.sourceLineCount += 1

        self.lineCount = 0
        self.sourceLineCount = 1
        while self.lineCount < len(self.listOfCodeLines):
            # K&R A 12.2
            self.lineSplicing()
            self.lineCount += 1
            self.sourceLineCount += 1

        self.lineCount = 0
        self.sourceLineCount = 1
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
            self.sourceLineCount += 1

        self.processedFile = ''.join(self.listOfCodeLines)
