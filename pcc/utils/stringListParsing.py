#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import print_function


def extract_closing_char(list_to_process, open_char, start_line, start_index,
                         closing_char):
    enclosed_string = ''
    carret = start_index
    current_line = start_line
    number_of_opening_chars = 0
    number_of_closing_chars = 0

    while current_line < len(list_to_process):
        while carret < len(list_to_process[current_line]):
            char = list_to_process[current_line][carret]
            # complete string found
            if char == closing_char:
                if number_of_closing_chars == (number_of_opening_chars - 1):
                    return current_line, carret
                number_of_closing_chars += 1
            # add the character to the string being build
            if number_of_opening_chars > 0:
                enclosed_string += char

            if char == open_char:
                number_of_opening_chars += 1
            carret += 1

        current_line += 1
        carret = 0
    # no enclosed string found
    return -1, -1
