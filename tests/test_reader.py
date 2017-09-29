"""Tests the csv reading functionality."""
import unittest
from unittest import mock
from minfluxdbconvert import reader as reader

class TestTransactionReader(unittest.TestCase):
    """Test the TransactionReader class."""

    @mock.patch('minfluxdbconvert.yaml.os.path.isfile')
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

    @mock.patch('minfluxdbconvert.yaml.os.path.isfile')
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

    def test_file_not_exist(self):
        with self.assertRaises(SystemExit) as cm:
            self.Reader = reader.TransactionReader('/tmp/fake')
        self.assertEqual(cm.exception.code, 1)
            
