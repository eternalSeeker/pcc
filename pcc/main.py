#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Program entry point"""

from __future__ import print_function

import argparse
import sys

from pcc import metadata
from pcc.preprocessor.preprocess import Preprocessor
from pcc.AST.ast import Ast


def main(argv):
    """Program entry point.

    :param argv: command-line arguments
    :type argv: :class:`list`
    """
    author_strings = []
    for name, email in zip(metadata.authors, metadata.emails):
        author_strings.append('Author: {0} <{1}>'.format(name, email))

    epilog = '''
{project} {version}

{authors}
URL: <{url}>
'''.format(
        project=metadata.project,
        version=metadata.version,
        authors='\n'.join(author_strings),
        url=metadata.url)

    arg_parser = argparse.ArgumentParser(
        prog=argv[0],
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=metadata.description,
        epilog=epilog)
    arg_parser.add_argument(
        "filesToProcess")
    arg_parser.add_argument(
        '-V', '--version',
        action='version',
        version='{0} {1}'.format(metadata.project, metadata.version))
    arg_parser.add_argument(
        '-I',
        help='directory to include',
        action='append')
    arg_parser.add_argument(
        '-E',
        help='only run the preprocessor',
        action='store_true')
    arg_parser.add_argument(
        '-fdump_tree',
        help='dump the AST',
        action='store_true')
    # ignore the name of the program
    arguments = arg_parser.parse_args(args=argv[1:])
    inputFile = arguments.filesToProcess
    includeDirs = arguments.I
    if arguments.I:
        includeDirs = arguments.I
    with open(inputFile, 'r') as fileToRead:
        inputFileAsString = fileToRead.read()
    preprocessor = Preprocessor(inputFile, inputFileAsString, includeDirs)
    preprocessor.preprocess()
    preprocessFileString = preprocessor.processedFile
    if arguments.E:
        # only perform the preprocessor step
        print(preprocessFileString, end='')
        return 0
    ast = Ast(preprocessFileString)
    result = ast.run_ast()
    if result != 0:
        return result
    if arguments.fdump_tree:
        print(ast.to_string(), end='')
    return 0


def entry_point():
    """Zero-argument entry point for use with setuptools/distribute."""
    raise SystemExit(main(sys.argv))


if __name__ == '__main__':
    entry_point()
