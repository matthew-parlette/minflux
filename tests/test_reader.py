"""Tests the csv reading functionality."""
import unittest
from unittest import mock
from minflux import reader as reader


class MockPathLib(object):
    """Mock class for pathlib library."""

    def __init__(self, dir):
        """Mock init."""
        pass

    @property
    def parent(self):
        """Mock pathlib.Path.parent."""
        return '/tmp'

    @property
    def name(self):
        """Mock pathlib.Path.name."""
        return 'bar.foo'

    @property
    def stem(self):
        """Mock pathlib.Path.stem."""
        return '.foo'

    def mkdir(self, parents=False, exist_ok=False):
        """Mock pathlib.Path.mkdir method."""
        return None


@mock.patch('minflux.yaml.os.path.isfile')
class TestTransactionReader(unittest.TestCase):
    """Test the TransactionReader class."""

    def setUp(self):
        """Initialization before test."""
        self.mock_csv_read_return = [
            [
                'Date',
                'Category',
                'Description',
                'Amount',
                'Transaction Type',
                'Labels',
                'Notes',
                'Account Name'
            ],
            [
                '1/1/2017',
                'foo',
                'bar',
                '3.50',
                'debit',
                'nolabel'
                'nonote'
                'foobar'
            ]
        ]

    def tearDown(self):
        """Tears down setup after test."""
        self.mock_csv_read_return = list()

    @mock.patch('minflux.reader.csv.reader')
    def test_read_csv(self, mock_csv_read, mock_is_file):
        """Verifies read_csv function."""
        mock_is_file.return_value = True
        mock_csv_read.return_value = self.mock_csv_read_return
        mock_fh = mock.mock_open()
        with mock.patch('builtins.open', mock_fh, create=False):
            self.Reader = reader.TransactionReader('/tmp/fake')

        self.assertEqual(len(self.Reader.data), 1)
        self.assertEqual(self.Reader.data, [mock_csv_read.return_value[1]])
        for key in self.Reader.headers:
            self.assertTrue(self.Reader.headers[key] is not None)

    @mock.patch('minflux.reader.csv.reader')
    def test_extra_keys_in_data(self, mock_csv_read, mock_is_file):
        """Verfies no errors thrown if unexpected keys exist in data."""
        mock_is_file.return_value = True
        self.mock_csv_read_return[0].append('Extra')
        self.mock_csv_read_return[1].append('unknown')
        mock_csv_read.return_value = self.mock_csv_read_return
        mock_fh = mock.mock_open()
        with mock.patch('builtins.open', mock_fh, create=False):
            self.Reader = reader.TransactionReader('/tmp/fake')

        self.assertEqual(len(self.Reader.data), 1)
        self.assertEqual(self.Reader.data, [mock_csv_read.return_value[1]])
        for key in self.Reader.headers:
            self.assertTrue(self.Reader.headers[key] is not None)

    def test_file_not_exist(self, mock_is_file):
        """Checks that error thrown if file does not exist."""
        mock_is_file.return_value = False
        with self.assertRaises(SystemExit) as cm:
            self.Reader = reader.TransactionReader('/tmp/fake')
        self.assertEqual(cm.exception.code, 1)

    @mock.patch('minflux.reader.TransactionReader.archive')
    @mock.patch('minflux.reader.csv.reader')
    def test_archive_entry(self, mock_csv_read, mock_archive, mock_is_file):
        """Checks that archiving is attempted when flagged in config."""
        mock_archive.return_value = None
        mock_is_file.return_value = True
        mock_csv_read.return_value = self.mock_csv_read_return
        mock_fh = mock.mock_open()
        with mock.patch('builtins.open', mock_fh, create=False):
            self.Reader = reader.TransactionReader('/tmp/fake', archive=True)
        self.assertEqual(mock_archive.call_count, 1)

    @mock.patch('minflux.reader.pathlib')
    @mock.patch('minflux.reader.os.path.exists')
    @mock.patch('minflux.reader.csv.reader')
    def test_archive_exist_on_too_many_collisons(self,
                                                 mock_csv_read,
                                                 mock_exists,
                                                 mock_pathlib,
                                                 mock_is_file):
        """Checks that code exists if too many name collisions exist."""
        mock_pathlib.Path = MockPathLib
        mock_is_file.return_value = True
        mock_exists.return_value = True
        mock_csv_read.return_value = self.mock_csv_read_return
        mock_fh = mock.mock_open()
        with mock.patch('builtins.open', mock_fh, create=False):
            with self.assertRaises(SystemExit) as cm:
                self.Reader = reader.TransactionReader('/tmp/fake',
                                                       archive=True)
        self.assertEqual(cm.exception.code, 1)
        self.assertEqual(mock_exists.call_count, 257)
