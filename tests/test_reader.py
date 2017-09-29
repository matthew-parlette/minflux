"""Tests the csv reading functionality."""
import unittest
from unittest import mock
from minfluxdbconvert import reader as reader

class MockPathLib(object):
    def __init__(self, dir):
        pass
    @property
    def parent(self):
        return '/tmp'
    @property
    def name(self):
        return 'bar.foo'
    @property
    def stem(self):
        return '.foo'
    def mkdir(self, parents=False, exist_ok=False):
        return None

@mock.patch('minfluxdbconvert.yaml.os.path.isfile')
class TestTransactionReader(unittest.TestCase):
    """Test the TransactionReader class."""

    @mock.patch('minfluxdbconvert.reader.csv.reader')
    def test_read_csv(self, mock_csv_read, mock_is_file):
        mock_is_file.return_value = True
        mock_csv_read.return_value = [['Date',
                                       'Category',
                                       'Description',
                                       'Amount',
                                       'Transaction Type',
                                       'Labels',
                                       'Notes',
                                       'Account Name'],
                                       ['1/1/2017',
                                        'foo',
                                        'bar',
                                        '3.50',
                                        'debit',
                                        'nolabel'
                                        'nonote'
                                        'foobar'
                                       ]]
        mock_fh = mock.mock_open()
        with mock.patch('builtins.open', mock_fh, create=False):
            self.Reader = reader.TransactionReader('/tmp/fake')

        self.assertEqual(len(self.Reader.data), 1)
        self.assertEqual(self.Reader.data, [mock_csv_read.return_value[1]])
        for key in self.Reader.headers:
            self.assertTrue(self.Reader.headers[key] is not None)

    @mock.patch('minfluxdbconvert.reader.csv.reader')
    def test_extra_keys_in_data(self, mock_csv_read, mock_is_file):
        mock_is_file.return_value = True
        mock_csv_read.return_value = [['Date',
                                       'Category',
                                       'Description',
                                       'Amount',
                                       'Transaction Type',
                                       'Labels',
                                       'Notes',
                                       'Account Name',
                                       'Extra'],
                                       ['1/1/2017',
                                        'foo',
                                        'bar',
                                        '3.50',
                                        'debit',
                                        'nolabel'
                                        'nonote'
                                        'foobar',
                                        'unknown'
                                       ]]
        mock_fh = mock.mock_open()
        with mock.patch('builtins.open', mock_fh, create=False):
            self.Reader = reader.TransactionReader('/tmp/fake')

        self.assertEqual(len(self.Reader.data), 1)
        self.assertEqual(self.Reader.data, [mock_csv_read.return_value[1]])
        for key in self.Reader.headers:
            self.assertTrue(self.Reader.headers[key] is not None)

    def test_file_not_exist(self, mock_is_file):
        mock_is_file.return_value = False
        with self.assertRaises(SystemExit) as cm:
            self.Reader = reader.TransactionReader('/tmp/fake')
        self.assertEqual(cm.exception.code, 1)

    @mock.patch('minfluxdbconvert.reader.TransactionReader.archive')
    @mock.patch('minfluxdbconvert.reader.csv.reader')
    def test_archive_entry(self, mock_csv_read, mock_archive, mock_is_file):
        mock_archive.return_value = None
        mock_is_file.return_value = True
        mock_csv_read.return_value = [['Date',
                                       'Category',
                                       'Description',
                                       'Amount',
                                       'Transaction Type',
                                       'Labels',
                                       'Notes',
                                       'Account Name'],
                                       ['1/1/2017',
                                        'foo',
                                        'bar',
                                        '3.50',
                                        'debit',
                                        'nolabel'
                                        'nonote'
                                        'foobar'
                                       ]]
        mock_fh = mock.mock_open()
        with mock.patch('builtins.open', mock_fh, create=False):
            self.Reader = reader.TransactionReader('/tmp/fake', archive=True)
        self.assertEqual(mock_archive.call_count, 1)
    
    @mock.patch('minfluxdbconvert.reader.pathlib')
    @mock.patch('minfluxdbconvert.reader.os.path.exists')
    @mock.patch('minfluxdbconvert.reader.csv.reader')
    def test_archive_exist_on_too_many_collisons(self, mock_csv_read, mock_exists, mock_pathlib, mock_is_file):
        mock_pathlib.Path = MockPathLib
        mock_is_file.return_value = True
        mock_exists.return_value = True
        mock_csv_read.return_value = [['Date',
                                       'Category',
                                       'Description',
                                       'Amount',
                                       'Transaction Type',
                                       'Labels',
                                       'Notes',
                                       'Account Name'],
                                       ['1/1/2017',
                                        'foo',
                                        'bar',
                                        '3.50',
                                        'debit',
                                        'nolabel'
                                        'nonote'
                                        'foobar'
                                       ]]
        mock_fh = mock.mock_open()
        with mock.patch('builtins.open', mock_fh, create=False):
            with self.assertRaises(SystemExit) as cm:
                self.Reader = reader.TransactionReader('/tmp/fake', archive=True)
        self.assertEqual(cm.exception.code, 1)        
        self.assertEqual(mock_exists.call_count, 257)