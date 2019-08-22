#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Program entry point"""

from __future__ import print_function

import argparse
import os
import sys

from pcc import metadata
from pcc.AST.ast import Ast
from pcc.compiler.compiler import Compiler
from pcc.preprocessor.preprocess import Preprocessor


def main(argv):
    """Start the program.

    Args:
        argv ([str]): command-line arguments

    Returns:
        int: error code, 0 if successful
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
    input_file = arguments.filesToProcess
    include_dirs = arguments.I

    output_file_name = os.path.basename(input_file)
    output_file_name = os.path.splitext(output_file_name)[0] + '.o'
    if arguments.o:
        output_file_name = arguments.o
    if arguments.I:
        include_dirs = arguments.I
    with open(input_file, 'r') as fileToRead:
        input_file_as_string = fileToRead.read()
    preprocessor = Preprocessor(input_file, input_file_as_string, include_dirs)
    preprocessor.preprocess()
    preprocess_file_string = preprocessor.processed_file
    if arguments.E:
        # only perform the preprocessor step
        print(preprocess_file_string, end='')
        return 0
    ast = Ast(preprocess_file_string, input_file)
    result = ast.run_ast()
    if result != 0:
        return result
    if arguments.fdump_tree:
        print(ast.__str__(), end='')
        return 0
    compiler = Compiler(input_file, ast.root_node)
    compiler.compile()
    if arguments.c:
        compiler.write_object_file_to_file(output_file_name)
        return 0
    return 0


def entry_point():
    """Zero-argument entry point for use with setuptools/distribute.

    Raises:
        SystemExit: setting the error code
    """
    raise SystemExit(main(sys.argv))


if __name__ == '__main__':
    entry_point()
