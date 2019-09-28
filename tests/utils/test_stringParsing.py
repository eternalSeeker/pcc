#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pcc.utils.stringParsing


class HelperTestObjects:
    def __init__(self, input_string, start_index, output_string):
        self.inputString = input_string
        self.startIndex = start_index
        self.outputString = output_string
        self.testObjects = []


class TestStringParsing(object):

    def setup_tests(self):
        self.testObjects = []

        obj = HelperTestObjects('find the string(this)', 0, 'this')
        self.testObjects.append(obj)

        obj = HelperTestObjects('find the string(this(with enclosure))', 0,
                          'this(with enclosure)')
        self.testObjects.append(obj)

        obj = HelperTestObjects('find the(not this) string(this)', 20, 'this')
        self.testObjects.append(obj)

    def test_extract_text_for_enclosed_parenthesis(self):
        self.setup_tests()
        for obj in self.testObjects:
            input_line = obj.inputString
            start_index = obj.startIndex
            output = pcc.utils.stringParsing. \
                extract_text_for_enclosed_parenthesis(input_line, start_index)
            assert output == obj.outputString
