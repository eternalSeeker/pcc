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


def preprocess(file):
    with open(file, 'r') as fileToRead:
        inputFileAsString = fileToRead.read()
    trigraphRelaced = runTrigraphReplacement(inputFileAsString)

    return trigraphRelaced
