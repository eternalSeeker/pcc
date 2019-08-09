#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import print_function

import sys


def warning(file_name, line_number, message):
    """Print a warning message.

    Args:
        file_name (str): the name of the file which caused the warning
        line_number (int): the line in the file which caused the warning
        message (str): the waring message
    """
    message_string = 'warning: file %s line %d, %s' % (file_name, line_number,
                                                       message)
    print(message_string)


def error(file_name, line_number, message):
    """Print a error message.

    Args:
        file_name (str): the name of the file which caused the error
        line_number (int): the line in the file which caused the error
        message (str): the error message
    """
    message_string = 'ERROR: file %s line %d, %s' % (file_name, line_number,
                                                     message)
    print(message_string, file=sys.stderr)
