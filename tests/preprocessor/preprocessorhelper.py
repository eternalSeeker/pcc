import subprocess
from os.path import join

from pcc.main import main


def generate_preprocessor_outputs(files_to_test, folder_path, option_arg=None):
    for file in files_to_test:
        file_input_path = join(folder_path, 'input', file)
        file_output_path = join(folder_path, 'output', file)
        command = 'gcc -E %s %s' % (
            option_arg if option_arg is not None else '', file_input_path)

        response = subprocess.run(command, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, shell=True)
        # decode the outputted string to ascii and split the line while
        # keeping the new line character(s)
        captured_result = response.stdout.decode('ascii').splitlines(True)

        if response:
            if response.returncode == 0:
                with open(file_output_path, 'w') as f:
                    for output_line in captured_result:
                        if '#' not in output_line:
                            f.write(output_line)
            else:
                print('ERROR checking %s, got <%s>' % (file, response.stderr))


class PreprocessorHelper(object):

    @staticmethod
    def execute_test(file_to_test, capsys, path_of_files,
                     include_dirs=None):
        """Execute the tests for the preprocessor.

        Args:
            file_to_test (str): the file to test
            capsys (method): the capsys fixture from pytest
            path_of_files (str): the path of the
            include_dirs (Union[str, None]): the include command line
                argument if needed
        """
        input_path = 'input'
        output_path = 'output'
        input_path = join(path_of_files, input_path)
        output_path = join(path_of_files, output_path)

        file_to_preprocess = file_to_test
        input_file_with_path = join(input_path, file_to_preprocess)
        output_file_with_path = join(output_path, file_to_preprocess)
        # this test will not raise SystemExit
        argsv = list(['progname'])
        argsv.append('-E')
        if include_dirs:
            argsv.extend(include_dirs)
        argsv.append(input_file_with_path)
        main(argsv)
        out, err = capsys.readouterr()
        with open(output_file_with_path, 'r') as fileToRead:
            output_file_as_string = fileToRead.read()
        # the outputted file needs to match exactly
        output_file_as_string = output_file_as_string.replace('\r', '')
        output_list = out.split('\n')
        output_file_as_list = output_file_as_string.split('\n')
        output_list_size = len(output_list)
        output_file_as_list_size = len(output_file_as_list)
        assert output_list_size == output_file_as_list_size, \
            'for file %s, size %d(got) != %d(req), got <%s> should be <%s>' % \
            (file_to_preprocess, output_list_size, output_file_as_list_size,
             out, output_file_as_string)
        for i in range(output_file_as_list_size):
            assert output_list[i] == output_file_as_list[i], \
                'for file %s line %d, <%s> != <%s>' % \
                (file_to_preprocess, i, output_list, output_file_as_list)
        # there should be no error
        assert err == ''
