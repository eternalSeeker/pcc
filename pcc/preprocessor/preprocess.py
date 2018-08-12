#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy


trigraphs = {
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


def runTrigraphReplacement(inputFileAsString):
    trigraphRelaced = copy.copy(inputFileAsString)
    for key in trigraphs.keys():
        trigraphRelaced = trigraphRelaced.replace(key, trigraphs[key])
    return trigraphRelaced


def lineSplicing(inputFileAsString):
    lineSpliced = copy.copy(inputFileAsString)
    backslashAndNewline = '\\\n'
    lineSpliced = lineSpliced.replace(backslashAndNewline, '')

    return lineSpliced


def preprocess(inputFileAsString):
    trigraphRelaced = runTrigraphReplacement(inputFileAsString)
    lineSpliced = lineSplicing(trigraphRelaced)
    return lineSpliced
