#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function


def extractTextForEnclosedParenthesis(string, startIndex):
    enclosedString = ''
    carret = startIndex
    numberOfOpeningParentheses = 0
    numberOfClosingParentheses = 0

    while carret < len(string):
        char = string[carret]
        # complete string found
        if char == ')':
            if numberOfClosingParentheses == (numberOfOpeningParentheses - 1):
                return enclosedString
            numberOfClosingParentheses += 1
        # add the character to the string being build
        if numberOfOpeningParentheses > 0:
            enclosedString += char

        if char == '(':
            numberOfOpeningParentheses += 1
        carret += 1
    # no enclosed string found
    return ''
