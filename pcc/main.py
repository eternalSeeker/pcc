#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Program entry point"""

from __future__ import print_function

import argparse
import sys
import os

from pcc import metadata
from pcc.preprocessor.preprocess import Preprocessor
from pcc.AST.ast import Ast
from pcc.compiler.compiler import Compiler


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
    arg_parser.add_argument(
        '-c',
        help='compile, no link',
        action='store_true')
    arg_parser.add_argument(
        '-o',
        type=str,
        help='output file name',
        action='store')
    # ignore the name of the program
    arguments = arg_parser.parse_args(args=argv[1:])
    inputFile = arguments.filesToProcess
    includeDirs = arguments.I

    output_file_name = os.path.basename(inputFile)
    output_file_name = os.path.splitext(output_file_name)[0] + '.o'
    if arguments.o:
        output_file_name = arguments.o
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
    ast = Ast(preprocessFileString, inputFile)
    result = ast.run_ast()
    if result != 0:
        return result
    if arguments.fdump_tree:
        print(ast.to_string(), end='')
        return 0
    compiler = Compiler(ast.root_node)
    compiler.compile()
    if arguments.c:
        compiler.write_object_file_to_file(output_file_name)
        return 0
    return 0


def entry_point():
    """Zero-argument entry point for use with setuptools/distribute."""
    raise SystemExit(main(sys.argv))


if __name__ == '__main__':
    entry_point()
