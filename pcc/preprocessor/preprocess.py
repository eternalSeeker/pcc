#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import os.path
import re

import pcc.utils.stringParsing
import pcc.utils.warning
from .ConstantExpression import ConstantExpression


class MacroObject:

    def __init__(self, identifier, argument_list, token_sequence):
        """Create a macro object

        Args:
            identifier (str): The name of the macro
            argument_list (List[str], optional): the list of macro arguments
            token_sequence (str): the tokens to replace the identifier
        """
        self.identifier = identifier
        self.token_sequence = token_sequence
        self.argument_list = argument_list

    def get_number_of_arguments(self):
        """Get the number of argments of the macro

        Returns:
            int: the number of arguments
        """
        return len(self.argument_list)

    def get_identifier(self):
        """Get the macro identifier

        Returns:
            str: the identifier
        """
        return self.identifier

    def get_token_sequence(self):
        """Get the token sequence

        Returns:
            str: the sequence
        """
        return self.token_sequence

    def fill_macro_in(self, arguments):
        """Return the macro subsitution with the supplied arguments

        Args:
            arguments (List[str]): the arguments for the macro

        Returns:
            str: the filled in macro
        """
        macro_string = self.token_sequence
        for i in range(len(self.argument_list)):
            macro_string = macro_string.replace(self.argument_list[i],
                                                arguments[i])

        return macro_string


class Preprocessor:

    def preprocessor_warning(self, message):
        """Generate a warning to the user for a line of source code

        Args:
            message (str): the waring message
        """
        pcc.utils.warning.warning(self.original_input_file_name,
                                  self.source_line_count, message)

    def preprocessor_error(self, message):
        """Generate an error to the user for a line of source code

        Args:
            message (str): the warning message
        """
        pcc.utils.warning.error(self.original_input_file_name,
                                self.source_line_count, message)

    @staticmethod
    def string_to_list_with_new_lines(source_string):
        """Convert to a list, keeping new lines.

        Args:
            source_string (str): the string to convert

        Returns:
            List[str]: the list of strings
        """
        source_file_list = source_string.split('\n')
        for i in range(len(source_file_list) - 1):
            source_file_list[i] += '\n'
        return source_file_list

    def replace_substring_on_current_line(self, old, new):
        """Replace the substring on the current line by the new substring

        Args:
            old (str): the substring to replace
            new (str): the new substring
        """
        self.list_of_code_lines[self.line_count] = \
            self.list_of_code_lines[self.line_count].replace(old, new)

    def __init__(self, input_file, input_file_string, include_dirs):
        """Create a preprocessor object.

        Args:
            input_file (str): the name of the file to preprocess
            input_file_string (str): the contents of the file to preprocess
            include_dirs (List[str]): the list of files to include if requested
        """
        self.original_input_file_name = input_file
        self.original_input_file = copy.copy(input_file_string)
        self.processed_file = ''
        self.tokens = dict()
        self.include_dirs = include_dirs
        self.list_of_code_lines = []
        self.line_count = 0
        self.source_line_count = 1
        self.trigraphs = {
            '??=': '#',
            '??/': '\\',
            '??\'': '^',
            '??(': '[',
            '??)': ']',
            '??!': '|',
            '??<': '{',
            '??>': '}',
            '??-': '~'
        }

    def run_trigraph_replacement(self):
        """Replace all trigraphs on the current line.

        """
        for key in self.trigraphs.keys():
            self.replace_substring_on_current_line(key, self.trigraphs[key])

    def line_splicing(self):
        """Merge spliced lines.

        """
        backslash_and_newline = '\\\n'
        current_line = self.list_of_code_lines[self.line_count]
        while backslash_and_newline in current_line:
            tmp = self.list_of_code_lines[self.line_count]. \
                replace(backslash_and_newline, '')

            self.list_of_code_lines[self.line_count] = \
                tmp + self.list_of_code_lines[self.line_count + 1]
            self.list_of_code_lines[self.line_count + 1] = '\n'
            self.source_line_count += 1
            current_line = self.list_of_code_lines[self.line_count]

    def include_files(self):
        if '#include' in self.list_of_code_lines[self.line_count]:
            # regex DOTALL dot also matches newline,
            # .*? any sequence of chars optional
            string_to_match = r'\s*?#include.*?\"(.*)\".*?'
            current_line = self.list_of_code_lines[self.line_count]
            match_flags = re.M | re.I | re.MULTILINE | re.DOTALL
            match_obj_quotes = re.match(string_to_match,
                                        current_line,
                                        match_flags)
            string_to_match = r'\s*?#include.*?<(.*)>.*?'
            current_line = self.list_of_code_lines[self.line_count]
            match_flags = re.M | re.I | re.MULTILINE | re.DOTALL
            match_obj_less_than = re.match(string_to_match,
                                           current_line,
                                           match_flags)
            if match_obj_quotes:
                self.fill_in_include(match_obj_quotes)
            elif match_obj_less_than:
                self.fill_in_include(match_obj_less_than)
            else:
                # no match, nothing to do
                self.preprocessor_warning('could not parse include statement')
                pass

    def fill_in_include(self, match_obj):
        """Replace the current line with the contents of the match object

        Args:
            match_obj (Match): the match object containing the filename of
                               the include
        """
        # there is an include in the file
        # get the filename from the match
        filename = match_obj.group(1)
        # add the current directory to the include dirs
        dirs_to_search = list(os.getcwd())
        if self.include_dirs:
            dirs_to_search.extend(self.include_dirs)
        is_file_found = False
        for dir_to_search in dirs_to_search:
            file_with_dir = os.path.join(dir_to_search, filename)
            if os.path.isfile(file_with_dir):
                # the file to include exists
                with open(file_with_dir, 'r') as fileToInclude:
                    self.replace_include_with_content_of_file(fileToInclude)
                    is_file_found = True
        if is_file_found is False:
            # error file does not exist
            self.preprocessor_error('file to include <%s> not found' %
                                    filename)

    def replace_include_with_content_of_file(self, file_to_include):
        """Replace the include with the contents of the file

        Args:
            file_to_include (file): the file handle of the include file
        """
        included_file = file_to_include.read()
        included_file = included_file.replace('\r', '')
        included_file_as_list = \
            self.string_to_list_with_new_lines(included_file)
        included_file_as_list[-1] += '\n'
        self.list_of_code_lines.pop(self.line_count)
        self.list_of_code_lines[self.line_count:self.line_count] = \
            included_file_as_list

    def remove_tokens(self):
        """Remove the tokens from the macro list for the matching undef.

        Returns:
            int: the number of source lines that are consumed
        """
        line_popped = False
        if '#undef' in self.list_of_code_lines[self.line_count]:
            match_obj = re.match(r'.*?#undef (.*)',
                                 self.list_of_code_lines[self.line_count],
                                 re.M | re.I | re.DOTALL)
            if match_obj:
                # remove all spaces and only look at the first element
                token_to_remove = match_obj.group(1).split()[0]
                if token_to_remove in self.tokens.keys():
                    self.tokens.pop(token_to_remove, None)
                    # remove the line of the undef statement
                    self.list_of_code_lines[self.line_count] = '\n'
                    self.source_line_count += 1
                    line_popped = True
                else:
                    self.preprocessor_error('token <%s> does not exist' %
                                            token_to_remove)
        return line_popped

    def macro_definition_and_expansion(self):
        """Add tokens to the macro list if found and expand macro's

        """
        # loop until there are no more lines removed from the list
        while True:
            line_popped = self.add_tokens()
            if line_popped is True:
                continue
            line_popped = self.remove_tokens()
            # if tokens are removed go back to to find new ones
            if line_popped is True:
                continue
            self.replace_tokens()
            break

    def is_conditional_compilation_flag_on_current_line(self):
        """Check if there is a conditional compilation flag in the current line

        Returns:
            bool: True if the a condition compilation flag is
                  on the current line
        """
        conditional_compilation_lines = ['#ifdef', '#ifndef', '#if ']
        for line_to_exclude in conditional_compilation_lines:
            if line_to_exclude in self.list_of_code_lines[self.line_count]:
                return True
        return False

    def replace_tokens(self):
        """Replace the macro tokens on the current line.

        """
        tokens_left = True
        while tokens_left and not \
                self.is_conditional_compilation_flag_on_current_line():
            tokens_left = False
            for token in self.tokens.keys():
                tokens_left = self.replace_token_if_found(token)

    def replace_token_if_found(self, token):
        """Replace macro tokens if found

        Args:
            token (str): the identifier of the token

        Returns:
            bool: True if there are
        """
        tokens_left = False
        if token in self.list_of_code_lines[self.line_count]:
            obj = self.tokens[token]
            if obj.get_number_of_arguments() == 0:
                token_sequence = obj.get_token_sequence()
                self.replace_substring_on_current_line(token, token_sequence)
            else:
                current_line = self.list_of_code_lines[self.line_count]
                start_index = current_line.find(token)
                argument_string = pcc.utils.stringParsing. \
                    extract_text_for_enclosed_parenthesis(current_line,
                                                          start_index)
                if argument_string.count(',') > 0:
                    args = argument_string.split(',')
                else:
                    args = list(argument_string)
                macro_string = obj.fill_macro_in(args)
                string_to_replace = token + '(' + argument_string + ')'
                self.replace_substring_on_current_line(string_to_replace,
                                                       macro_string)
            tokens_left = True
        return tokens_left

    def add_tokens(self):
        """Add macro tokens to the list if found

        Returns:
            bool: True if a token macro found and added to the list
        """
        line_popped = False
        while '#define' in self.list_of_code_lines[self.line_count]:
            match_obj = re.match(r'.*?#define (.*)',
                                 self.list_of_code_lines[self.line_count],
                                 re.M | re.I | re.DOTALL)
            if match_obj:
                list_of_tokens = match_obj.group(1).split()
                token = list_of_tokens[0]
                if '(' in token:
                    start_index = 0
                    extracted_string = pcc.utils.stringParsing. \
                        extract_text_for_enclosed_parenthesis(token,
                                                              start_index)
                    number_of_arguments = extracted_string.count(',') + 1
                    if number_of_arguments >= 1:
                        argument_list = extracted_string.split(',')
                    else:
                        argument_list = list(extracted_string)
                    identifier = token.split('(')[0]
                else:
                    identifier = token
                    argument_list = []

                if len(list_of_tokens) > 1:
                    # find the start of the sequence part of the Macro,
                    # by finding all occurrences for the substring
                    # 'list_of_tokens[1]' in the complete match object
                    # (this retains spacing information)
                    original_string = match_obj.group(1)
                    start_of_sequence_string = list_of_tokens[1]
                    starts = [match.start() for match in re.finditer(
                        re.escape(start_of_sequence_string), original_string)]
                    start_of_sequence = starts[-1]
                    token_sequence = original_string[start_of_sequence:]
                    token_sequence = token_sequence.replace('\n', '')
                else:
                    token_sequence = ''
                obj = MacroObject(identifier, argument_list, token_sequence)
                if identifier in self.tokens.keys():
                    self.preprocessor_error('Macro already defined')
                else:
                    self.tokens[identifier] = obj
                # clear the line that contained the define
                self.list_of_code_lines[self.line_count] = '\n'
                self.source_line_count += 1
                line_popped = True
        return line_popped

    def error_generation(self):
        """Generated the preprocessor error message

        """
        if '#error' in self.list_of_code_lines[self.line_count]:
            current_line = self.list_of_code_lines[self.line_count]
            match_obj = re.match(r'.*?#error(.*)',
                                 current_line,
                                 re.M | re.I | re.DOTALL)
            if match_obj:
                message = ''
                if match_obj.group(1):
                    message = match_obj.group(1)
                self.preprocessor_error(message)
                self.list_of_code_lines.pop(self.line_count)
                self.source_line_count += 1

    @staticmethod
    def evaluate_constant_expression(expression_string):
        """Evaluate the constant expression

        Args:
            expression_string (str): the constant expression string

        Returns:
            bool: the result of the constant expression
        """
        expression = ConstantExpression(expression_string)
        evaluation = expression.evaluate()
        return evaluation

    def condition_compilation(self):
        """Replace the preprocessor if.

        """
        if '#if' in self.list_of_code_lines[self.line_count]:
            if_line = self.list_of_code_lines[self.line_count]
            part_is_active = self.check_if_branch_is_active(if_line)
            finished = False
            number_of_nested_conditions = 0
            current_index = self.line_count + 1
            # add an empty line instead of the #if line
            code_to_include = ['\n']
            current_index, finished = \
                self.add_active_branch(code_to_include, current_index,
                                       finished, if_line,
                                       number_of_nested_conditions,
                                       part_is_active)
            if finished is False:
                message = 'could not find closing #endif'
                self.preprocessor_error(message)

            del self.list_of_code_lines[self.line_count: current_index]
            self.list_of_code_lines[self.line_count:self.line_count] = \
                code_to_include

    def add_active_branch(self, code_to_include, current_index, finished,
                          if_line, number_of_nested_conditions,
                          part_is_active):
        """Add the active branch of the source code

        Args:
            code_to_include (List[str]): the code to include
            current_index (int): the current line of source code
            finished (bool): True if finished
            if_line (str): the line with the if condition
            number_of_nested_conditions (int): the number of nested conditions
            part_is_active (bool): True if this part is active

        Returns:
            (int, bool): the new line number and if the parsing is finished
        """
        while finished is False and \
                current_index < len(self.list_of_code_lines):
            if '#endif' in self.list_of_code_lines[current_index]:
                finished, number_of_nested_conditions = \
                    self.process_endif(finished, number_of_nested_conditions,
                                       current_index)

            elif '#if' in self.list_of_code_lines[current_index]:
                number_of_nested_conditions += 1
            elif number_of_nested_conditions > 0:
                # add all in the nested part
                pass
            elif '#elif' in self.list_of_code_lines[current_index]:
                # if the part was active, add it
                # if the part was not active and  became active, do not
                #   add it
                # else it was not active so not add it
                # TODO not correct
                part_is_active = self.check_if_elif_is_active(if_line,
                                                              part_is_active)
            elif '#else' in self.list_of_code_lines[current_index]:
                # if the part was active, add it
                # if the part was not active and  became active, do not
                #   add it
                # else it was not active so not add it
                part_is_active = self.is_else_part_active(part_is_active)
                self.list_of_code_lines[current_index] = '\n'
            else:
                pass

            self.parse_line(code_to_include, current_index, part_is_active)

            current_index += 1
        return current_index, finished

    def process_endif(self, finished, number_of_nested_conditions,
                      current_index):
        """Process a line containing an endif.

        Args:
            finished (bool): True if finished
            number_of_nested_conditions (int): the number of nested conditions
            current_index (int): the current line number

        Returns:
            (bool, int): the finished condition and the number of nested
                         conditions
        """
        if number_of_nested_conditions == 0:
            finished = True
            self.list_of_code_lines[current_index] = '\n'
        else:
            number_of_nested_conditions -= 1
        return finished, number_of_nested_conditions

    def parse_line(self, code_to_include, current_index, part_is_active):
        """Parse the line.

        Args:
            code_to_include (List[str]): the list of code to include
            current_index (int): the current line of code
            part_is_active (bool): True if this part is active
        """
        if part_is_active is True:
            code_to_include.append(self.list_of_code_lines[current_index])
        else:
            pass

    @staticmethod
    def is_else_part_active(part_is_active):
        """Return if the else part is active knowing the if part is active

        Args:
            part_is_active (bool): True if the if part is active

        Returns:
            bool: True if the else part, else None
        """
        if part_is_active is False:
            part_is_active = True
        elif part_is_active is True:
            part_is_active = None
        return part_is_active

    def check_if_elif_is_active(self, if_line, part_is_active):
        """Check if the elif is active

        Args:
            if_line (str): the line with the condition
            part_is_active (bool): if the if part is active

        Returns:
            bool: True if the else part is active
        """
        if part_is_active is True:
            part_is_active = None
        elif part_is_active is False:
            expression = if_line.split('#elif ')[1]
            part_is_active = self.evaluate_constant_expression(expression)
        return part_is_active

    def check_if_branch_is_active(self, if_line):
        """check the branches of the conditional compilation

        Args:
            if_line (str): the line with the condition

        Returns:
            bool: True if the if branch is active
        """
        if '#ifdef' in if_line:
            identifier = if_line.split('#ifdef')[1]
            identifier = ''.join(identifier.split())

            if identifier in self.tokens.keys():
                part_is_active = True
            else:
                part_is_active = False
        elif '#ifndef' in if_line:
            identifier = if_line.split('#ifndef')[1]
            identifier = ''.join(identifier.split())
            if identifier not in self.tokens.keys():
                part_is_active = True
            else:
                part_is_active = False

        else:
            expression = if_line.split('#if ')[1]
            part_is_active = \
                self.evaluate_constant_expression(expression)
        return part_is_active

    def preprocess(self):
        """Run the preprocessor.

        """
        source_file = copy.copy(self.original_input_file)
        # Remove all carriage returns if present in the file
        source_file = source_file.replace('\r', '')
        # split the source file in lines of code
        # but do not remove the '\n' char
        list_of_code = self.string_to_list_with_new_lines(source_file)
        self.list_of_code_lines = copy.copy(list_of_code)

        self.line_count = 0
        self.source_line_count = 1
        while self.line_count < len(self.list_of_code_lines):
            # K&R A 12.1
            self.run_trigraph_replacement()
            self.line_count += 1
            self.source_line_count += 1

        self.line_count = 0
        self.source_line_count = 1
        while self.line_count < len(self.list_of_code_lines):
            # K&R A 12.2
            self.line_splicing()
            self.line_count += 1
            self.source_line_count += 1

        self.line_count = 0
        self.source_line_count = 1
        while self.line_count < len(self.list_of_code_lines):
            # K&R A 12.3
            self.macro_definition_and_expansion()
            # K&R A 12.4
            self.include_files()
            # K&R A 12.5
            self.condition_compilation()
            # K&R A 12.7
            self.error_generation()
            self.line_count += 1
            self.source_line_count += 1

        self.processed_file = ''.join(self.list_of_code_lines)
