#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pcc.utils.stringParsing


class testObjects:
    def __init__(self, inputString, startIndex, outputString):
        self.inputString = inputString
        self.startIndex = startIndex
        self.outputString = outputString
        self.testObjects = []


class TestStringParsing(object):

    def setupTests(self):
        self.testObjects = []

        obj = testObjects('find the string(this)', 0, 'this')
        self.testObjects.append(obj)

        obj = testObjects('find the string(this(with enclosure))', 0,
                          'this(with enclosure)')
        self.testObjects.append(obj)

        obj = testObjects('find the(not this) string(this)', 20, 'this')
        self.testObjects.append(obj)

    def test_extractTextForEnclosedParenthesis(self):
        self.setupTests()
        for obj in self.testObjects:
            inputLine = obj.inputString
            startIndex = obj.startIndex
            output = pcc.utils.stringParsing. \
                extract_text_for_enclosed_parenthesis(inputLine, startIndex)
            assert output == obj.outputString
