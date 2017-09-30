"""Tests the json building functionality."""
import unittest
from unittest import mock
from minflux import json as json


class MockReader(object):
    """Class used to mock the reader module."""

    def __init__(self, file, archive=False, archive_dir=None):
        """Initialize MockReader class."""
        self.headers = {
            'date': 0,
            'description': 1,
            'account_name': 2,
            'transaction_type': 3,
            'amount': 4,
            'category': 5,
            'labels': 6,
            'notes': 7
        }
        self.data = [
            [
                '1/1/1970',
                'foo',
                'bar',
                'credit',
                '3.50',
                'foocat',
                'foolabel',
                'barnote'
            ],
            [
                '1/2/1970',
                'oof',
                'rab',
                'debit',
                '1.25',
                'tacoof',
                'lebaloof',
                'etonrab'
            ]
        ]


class TestJsonify(unittest.TestCase):
    """Test jsonify functionality."""

    def setUp(self):
        """Sets up common entries for testing."""
        self.json = {'tags': {}}
        self.headers = {
            'category': 0,
            'description': 1,
            'account_name': 2
        }
        self.entry = ['foo', 'bar', 'foobar']

        self.entry_2 = ['pass', 'pass', 'pass']

        self.netsum_config = {
            'exclude': {
                'vendor': [],
                'category': [],
                'account': []
            }
        }

    def tearDown(self):
        """Tears down common entries for testing."""
        self.json = dict()
        self.headers = dict()
        self.entry = list()
        self.entry_2 = list()
        self.netsum_config = dict()

    def test_sort_by_category(self):
        """Verifies json sorted by category."""
        json_expected = {
            'measurement': 'foo',
            'tags': {
                'vendor': 'bar',
                'account': 'foobar'
            }
        }

        self.assertEqual(json.sort_by_category(self.json,
                                               self.entry,
                                               self.headers),
                         json_expected)

    def test_sort_by_vendor(self):
        """Verifies json sorted by vendor."""
        json_expected = {
            'measurement': 'bar',
            'tags': {
                'category': 'foo',
                'account': 'foobar'
            }
        }

        self.assertEqual(json.sort_by_vendor(self.json,
                                             self.entry,
                                             self.headers),
                         json_expected)

    def test_sort_by_account(self):
        """Verifies json sorted by account."""
        json_expected = {
            'measurement': 'foobar',
            'tags': {
                'vendor': 'bar',
                'category': 'foo'
            }
        }

        self.assertEqual(json.sort_by_account(self.json,
                                              self.entry,
                                              self.headers),
                         json_expected)

    def test_net_sum_no_exclude(self):
        """Verifies amounts properly summed given no exclusions in config."""
        value = 0
        value += json.check_entry_for_net_sum(self.netsum_config,
                                              self.entry,
                                              self.headers, 1)
        value += json.check_entry_for_net_sum(self.netsum_config,
                                              self.entry_2,
                                              self.headers, 3)
        self.assertEqual(value, 4)

    def test_net_sum_with_exclude(self):
        """Verifies amounts properly summed given exclusions in config."""
        value = 0
        self.netsum_config['exclude']['vendor'] = ['bar']
        value += json.check_entry_for_net_sum(self.netsum_config,
                                              self.entry,
                                              self.headers, 1)
        value += json.check_entry_for_net_sum(self.netsum_config,
                                              self.entry_2,
                                              self.headers, 3)
        self.assertEqual(value, 3, msg='{}'.format(self.netsum_config))

    def test_netsum_json_entry(self):
        """Verifies date and value of net_sum."""
        all_dates = [
            '1970-01-01T00:00:00+00:00',
            '1970-01-02T00:00:00+00:00',
            '1970-01-03T00:00:00+00:00'
        ]
        returned_entry = json.net_sum_entry(5, all_dates)
        self.assertEqual(returned_entry['time'], all_dates[0])
        self.assertEqual(returned_entry['fields']['value'], 5)
        self.assertEqual(returned_entry['measurement'], 'net_sum')

    @mock.patch('minflux.json.reader')
    def test_jsonify(self, mock_reader):
        """Verifies keys/values properly set in json body."""
        mock_reader.TransactionReader = MockReader
        body = json.jsonify({'net_sum': self.netsum_config}, '/tmp/notreal')
        self.assertEqual(len(body), 7)
        self.assertEqual(body[-1]['measurement'], 'net_sum')
        self.assertEqual(body[-1]['fields']['value'], 2.25)

    @mock.patch('minflux.json.reader')
    def test_archive_single_file_custom_dir(self, mock_reader):
        """Verify we don't cause errors in this mode."""
        mock_reader.TransactionReader = MockReader
        config = {
            'mint': {
                'file': '/foo.csv',
                'archive': {
                    'directory': '/tmp'
                }
            }
        }
        body = json.jsonify(config, '/foo.csv')
        self.assertEqual(len(body), 7)

    @mock.patch('minflux.json.reader')
    def test_archive_dir_custom_dir(self, mock_reader):
        """Verify we don't cause errors in this mode."""
        mock_reader.TransactionReader = MockReader
        config = {
            'mint': {
                'directory': '/foo',
                'archive': {
                    'directory': '/tmp'
                }
            }
        }
        body = json.jsonify(config, '/foo/bar.csv')
        self.assertEqual(len(body), 7)

    @mock.patch('minflux.json.reader')
    def test_no_archive_dir(self, mock_reader):
        """Verify we don't cause errors in this mode."""
        mock_reader.TransactionReader = MockReader
        config = {
            'mint': {
                'directory': '/foo',
                'archive': {}
            }
        }
        body = json.jsonify(config, '/foo/bar.csv')
        self.assertEqual(len(body), 7)
