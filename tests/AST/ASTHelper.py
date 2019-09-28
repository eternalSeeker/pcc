
import pycparser
from os.path import join
from pcc.main import main


def generate_ast_outputs(files_to_test, folder_path):
    for file in files_to_test:

        file_input_path = join(folder_path, 'input', file)
        file_output_path = join(folder_path, 'output', file)

        output_buffer = open(file_output_path, 'w')
        ast = pycparser.parse_file(file_input_path, use_cpp=False)
        ast.show(buf=output_buffer, showcoord=False)
        output_buffer.close()


class ASTHelper(object):

    @staticmethod
    def execute_test(file_to_test, capsys, path_of_files):
        """Execute the tests for the preprocessor.

        Args:
            file_to_test (str): the file to test
            capsys (method): the capsys fixture from pytest
            path_of_files (str): the path of the
        """
        include_dirs = []
        input_path = 'input'
        output_path = 'output'
        input_path = join(path_of_files, input_path)
        output_path = join(path_of_files, output_path)

        file_to_preprocess = file_to_test
        input_file_with_path = join(input_path, file_to_preprocess)
        output_file_with_path = join(output_path, file_to_preprocess)
        # this test will not raise SystemExit
        argsv = list(['progname'])
        argsv.append('-fdump_tree')
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
            'for file %s, size %d != %d \n(%s)' % \
            (file_to_preprocess, output_list_size, output_file_as_list_size,
             out)
        for i in range(output_file_as_list_size):
            assert output_list[i] == output_file_as_list[i], \
                'for file %s line %d, <%s> != <%s>' % \
                (file_to_preprocess, i, output_list[i], output_file_as_list[i])
        # there should be no error
        assert err == ''
