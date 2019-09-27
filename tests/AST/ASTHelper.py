
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
        includeDirs = []
        inputPath = 'input'
        outputPath = 'output'
        inputPath = join(path_of_files, inputPath)
        outputPath = join(path_of_files, outputPath)

        fileToPreprocess = file_to_test
        inputFileWithPath = join(inputPath, fileToPreprocess)
        outputFileWithPath = join(outputPath, fileToPreprocess)
        # this test will not raise SystemExit
        argsv = list(['progname'])
        argsv.append('-fdump_tree')
        argsv.extend(includeDirs)
        argsv.append(inputFileWithPath)
        main(argsv)
        out, err = capsys.readouterr()
        with open(outputFileWithPath, 'r') as fileToRead:
            outputFileAsString = fileToRead.read()
        # the outputted file needs to match exactly
        outputFileAsString = outputFileAsString.replace('\r', '')
        outputList = out.split('\n')
        outputFileAsList = outputFileAsString.split('\n')
        outputListSize = len(outputList)
        outputFileAsListSize = len(outputFileAsList)
        assert outputListSize == outputFileAsListSize, \
            'for file %s, size %d != %d \n(%s)' % \
            (fileToPreprocess, outputListSize, outputFileAsListSize,
             out)
        for i in range(outputFileAsListSize):
            assert outputList[i] == outputFileAsList[i], \
                'for file %s line %d, <%s> != <%s>' % \
                (fileToPreprocess, i, outputList[i], outputFileAsList[i])
        # there should be no error
        assert err == ''
