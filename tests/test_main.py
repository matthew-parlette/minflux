"""Tests main functionality."""
import unittest
from unittest import mock
from minfluxdbconvert import __main__ as main

class TestMainModule(unittest.TestCase):
       
    def test_no_arguments(self):
        with self.assertRaises(SystemExit) as cm:
            main.main()
        self.assertEqual(cm.exception.code, 2)

    @mock.patch('minfluxdbconvert.__main__.json.dumps')
    @mock.patch('minfluxdbconvert.__main__.jsonify')
    @mock.patch('minfluxdbconvert.__main__.yaml.load_yaml')
    def test_with_skip_db_push(self, mock_load_yaml, mock_jsonify, mock_json_dumps):
        test_args = ['mfdb', '--config=/tmp/fake/path', '--skip-push']
        mock_load_yaml.return_value = {
            'influx_db': {
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
        mock_jsonify.return_value = {'foo': 'bar'} 
        mock_json_dumps.return_value = 'foobar'
        with mock.patch('sys.argv', test_args):
            with self.assertRaises(SystemExit) as cm:
                mock_fh = mock.mock_open()
                with mock.patch('builtins.open', mock_fh, create=False):
                    main.main()
            self.assertEqual(cm.exception.code, None)        
        