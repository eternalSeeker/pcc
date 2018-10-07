#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys


def warning(fileName, lineNumber, message):
    messageString = 'warning: file %s line %d, %s' % (fileName, lineNumber,
                                                      message)
    print(messageString)


def error(fileName, lineNumber, message):
        messageString = 'ERROR: file %s line %d, %s' % (fileName, lineNumber,
                                                        message)
        print(messageString, file=sys.stderr)
