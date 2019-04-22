#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import print_function


def extract_text_for_enclosed_parenthesis(string, start_index):
    enclosed_string = ''
    carret = start_index
    number_of_opening_parentheses = 0
    number_of_closing_parentheses = 0

    while carret < len(string):
        char = string[carret]
        # complete string found
        if char == ')':
            if number_of_closing_parentheses == \
                    (number_of_opening_parentheses - 1):
                return enclosed_string
            number_of_closing_parentheses += 1
        # add the character to the string being build
        if number_of_opening_parentheses > 0:
            enclosed_string += char

        if char == '(':
            number_of_opening_parentheses += 1
        carret += 1
    # no enclosed string found
    return ''
