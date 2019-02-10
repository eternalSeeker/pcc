# -*- coding: utf-8 -*-
from pytest import raises


from pcc import metadata
from pcc.main import main

# The parametrize function is generated, so it does not work to import
import pytest
parametrize = pytest.mark.parametrize


class TestMain(object):
    @parametrize('helparg', ['-h', '--help'])
    def test_help(self, helparg, capsys):
        with raises(SystemExit) as exc_info:
            main(['progname', helparg])
        out, err = capsys.readouterr()
        # Should have printed some sort of usage message. We don't
        # need to explicitly test the content of the message.
        assert 'usage' in out
        # Should have used the program name from the argument
        # vector.
        assert 'progname' in out
        # Should exit with zero return code.
        assert exc_info.value.code == 0

    @parametrize('versionarg', ['-V', '--version'])
    def test_version(self, versionarg, capsys):
        with raises(SystemExit) as exc_info:
            main(['progname', versionarg])
        captured = capsys.readouterr()
        # Should print out version.
        assert captured.err == ''
        assert captured.out == '{0} {1}\n'. \
            format(metadata.project, metadata.version)
        # Should exit with zero return code.
        assert exc_info.value.code == 0
