#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pcc.utils.stringListParsing import extract_closing_char
import pytest
parametrize = pytest.mark.parametrize

case1 = (['[', 'this', ']'],
         '[',
         0,
         0,
         ']',
         2,
         0)
case2 = (['[', 'this', ']'],
         '[',
         0,
         0,
         '}',
         -1,
         -1)


test_cases = [
    case1,
    case2
]


class TestStringParsing(object):

    @parametrize('input_list,start_char,start_line,start_index,closing_char,'
                 'result_line,result_index',
                 test_cases)
    def test_extractTextForEnclosedParenthesis(self, input_list, start_char,
                                               start_line, start_index,
                                               closing_char, result_line,
                                               result_index):
        ret_line, ret_index = \
            extract_closing_char(input_list, start_char, start_line,
                                 start_index, closing_char)
        assert result_line == ret_line
        assert result_index == ret_index
