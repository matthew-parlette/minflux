"""Tests main functionality."""
import unittest
from unittest import mock
from minflux import __main__ as main


@mock.patch('minflux.__main__.dbwrite.influxdb_write')
@mock.patch('minflux.__main__.yaml.load_yaml')
class TestMainModule(unittest.TestCase):
    """Test functionality of main module."""

    def test_no_arguments(self, mock_load_data, mock_client):
        """Test for when no arguments supplied to script."""
        mock_load_data.return_value = {}
        mock_client.return_value = True
        with self.assertRaises(SystemExit) as cm:
            main.main()
        self.assertEqual(cm.exception.code, 2)

    def test_with_skip_db_push(self, mock_load_yaml, mock_client):
        """Checks that db write skipped when --skip-push flag set."""
        test_args = ['mfdb', '--config=/tmp/fake/path', '--skip-push']
        mock_client.return_value = True
        mock_load_yaml.return_value = {
            'influxdb': {
                'host': 'foo',
                'port': 1234,
                'user': 'foo',
                'password': 'bar',
                'dbname': 'foobar'
            },
            'mint': {
                'file': '/tmp/fake.csv'
            },
            'logger': {
                'file': '',
                'level': 'INFO'
            }
        }
        with mock.patch('sys.argv', test_args):
            mock_fh = mock.mock_open()
            with mock.patch('builtins.open', mock_fh, create=False):
                main.main()
        self.assertEqual(mock_client.call_count, 1)

    @mock.patch('minflux.__main__.glob.glob')
    def test_with_dir(self, mock_glob, mock_load_yaml, mock_client):
        """Tests handling of directory containing multiple csv files."""
        test_args = ['mfdb', '--config=/tmp/fake/path']
        mock_glob.return_value = ['foo.csv', 'bar.csv', 'foobar.csv']
        mock_client.return_value = True
        mock_load_yaml.return_value = {
            'influxdb': {
                'host': 'foo',
                'port': 1234,
                'user': 'foo',
                'password': 'bar',
                'dbname': 'foobar'
            },
            'mint': {
                'directory': '/foo/bar'
            },
            'logger': {
                'file': '',
                'level': 'INFO'
            }
        }
        with mock.patch('sys.argv', test_args):
            mock_fh = mock.mock_open()
            with mock.patch('builtins.open', mock_fh, create=False):
                main.main()
        self.assertEqual(mock_client.call_count, 3)

    @mock.patch('minflux.__main__.glob.glob')
    def test_bad_write(self, mock_glob, mock_load_yaml, mock_client):
        """Checks that we exit script on a failed db write."""
        test_args = ['mfdb', '--config=/tmp/fake/path']
        mock_client.return_value = False
        mock_glob.return_value = ['foo.csv', 'bar.csv', 'foobar.csv']
        mock_load_yaml.return_value = {
            'influxdb': {
                'host': 'foo',
                'port': 1234,
                'user': 'foo',
                'password': 'bar',
                'dbname': 'foobar'
            },
            'mint': {
                'directory': '/foo/bar'
            },
            'logger': {
                'file': '',
                'level': 'INFO'
            }
        }
        with mock.patch('sys.argv', test_args):
            with self.assertRaises(SystemExit) as cm:
                mock_fh = mock.mock_open()
                with mock.patch('builtins.open', mock_fh, create=False):
                    main.main()
            self.assertEqual(mock_client.call_count, 1)
            self.assertEqual(cm.exception.code, 1)
