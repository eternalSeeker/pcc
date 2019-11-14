import os
import subprocess
from os.path import join

from pcc.main import main


def generate_compiler_outputs(files_to_test, folder_path):
    for test_tuple in files_to_test:
        input_file = test_tuple[0]
        input_helper = test_tuple[1]
        output_file = test_tuple[2]
        file_input_path = join(folder_path, 'input', input_file)
        helper_input_path = join(folder_path, 'input', input_helper)
        file_output_path = join(folder_path, 'output', output_file)
        gcc_output_file_name = 'out.o'
        gcc_exe = join(folder_path, 'output', 'exe.out')
        command = 'gcc -c %s -o %s' % (file_input_path, gcc_output_file_name)

        subprocess.run(command, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, shell=True)

        command = 'gcc %s -o %s %s' % \
                  (helper_input_path, gcc_exe, gcc_output_file_name)

        response = subprocess.run(command, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, shell=True)
        assert response.returncode == 0, response.stderr
        command = gcc_exe
        response = subprocess.run(command, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, shell=True)
        assert response.returncode == 0, response.stderr
        # decode the outputted string to ascii and split the line while
        # keeping the new line character(s)
        captured_result = response.stdout.decode('ascii').splitlines(True)
        with open(file_output_path, 'w') as f:
            for output_line in captured_result:
                f.write(output_line)

        os.remove(gcc_exe)
        os.remove(gcc_output_file_name)


class CompilerHelper(object):

    def execute_test(self, input_file, helper_file, output_file, capsys,
                     path_of_files):
        """Execute the tests for the preprocessor.

        Args:
            input_file (str): the file to test
            helper_file (str): the helper file to test
            output_file (str): the output file of the test
            capsys (method): the capsys fixture from pytest
            path_of_files (str): the path of the
        """
        input_path = 'input'
        output_path = 'output'
        pcc_output_file_name = 'test.out'

        input_path = join(path_of_files, input_path)
        helper_path = join(path_of_files, 'input', helper_file)
        output_path = join(path_of_files, output_path)
        pcc_output_file_path = join(path_of_files, pcc_output_file_name)

        input_file_with_path = join(input_path, input_file)
        output_file_with_path = join(output_path, output_file)
        # this test will not raise SystemExit
        argsv = list(['progname'])
        argsv.append('-c')
        argsv.append('-o' + str(pcc_output_file_path))
        argsv.append(input_file_with_path)
        main(argsv)
        out, err = capsys.readouterr()
        assert out == ''
        # there should be no error
        assert err == ''

        gcc_exe = 'test'

        command = 'gcc %s -o %s %s' % \
                  (helper_path, gcc_exe, pcc_output_file_path)

        response = subprocess.run(command, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, shell=True)
        assert response.returncode == 0, response.stderr

        command = './' + gcc_exe
        response = subprocess.run(command, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, shell=True)

        assert response.returncode == 0, response.stderr

        # decode the outputted string to ascii and split the line while
        # keeping the new line character(s)
        captured_result = response.stdout.decode('ascii').splitlines(True)

        output_file_as_list, output_file_as_list_size = \
            self.extract_file_contents(output_file_with_path)

        captured_result = ''.join(captured_result)
        output_list = captured_result.split('\n')
        output_list_size = len(output_list)

        # the outputted file needs to match exactly
        assert output_list_size == output_file_as_list_size, \
            'for file %s, size %d != %d \n(%s)' % \
            (output_file, output_list_size, output_file_as_list_size,
             out)
        for i in range(output_file_as_list_size):
            assert output_list[i] == output_file_as_list[i], \
                'for file %s line %d, <%s> != <%s>' % \
                (output_file, i, output_list[i], output_file_as_list[i])

        os.remove(pcc_output_file_path)
        os.remove(gcc_exe)

    @staticmethod
    def extract_file_contents(output_file_with_path):
        with open(output_file_with_path, 'r') as fileToRead:
            output_file_as_string = fileToRead.read()
        output_file_as_string = output_file_as_string.replace('\r', '')
        output_file_as_list = output_file_as_string.split('\n')
        output_file_as_list_size = len(output_file_as_list)
        return output_file_as_list, output_file_as_list_size
