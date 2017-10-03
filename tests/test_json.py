"""Tests the json building functionality."""
import unittest
from unittest import mock
from minflux import json as json

DATA = [
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
        self.data = DATA


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

    @mock.patch('minflux.json.reader')
    def test_jsonify(self, mock_reader):
        """Verifies keys/values properly set in json body."""
        mock_reader.TransactionReader = MockReader
        body = json.jsonify({'mint': {}, 'net_sum': self.netsum_config},
                            '/tmp/notreal')
        self.assertEqual(len(body), 7, msg=body)
        self.assertEqual(body[-1]['measurement'], 'net_sum')
        self.assertEqual(body[-1]['fields']['value'], 2.25)
        measurement_keys = [
            DATA[0][1],
            DATA[0][2],
            DATA[0][5],
            DATA[1][1],
            DATA[1][2],
            DATA[1][5]
        ]

        # Make a measurement counter
        measurement_counter = dict()
        for key in measurement_keys:
            measurement_counter[key] = 0
        for entry in body:
            for key in measurement_keys:
                if entry['measurement'] == key:
                    measurement_counter[key] += 1

        for key in measurement_keys:
            self.assertEqual(measurement_counter[key], 1)

    def test_get_sum_entries(self):
        """Tests ability to sum across measurements."""
        body_mock = [
            {
                'measurement': 'foo',
                'time': '1970-01-01T00:00:00+00:00',
                'fields': {
                    'value': 1.00
                }
            },
            {
                'measurement': 'foo',
                'time': '1970-01-02T00:00:00+00:00',
                'fields': {
                    'value': 1.50
                }
            },
            {
                'measurement': 'bar',
                'time': '1970-01-03T00:00:00+00:00',
                'fields': {
                    'value': 2.00
                }
            },
            {
                'measurement': 'bar',
                'time': '1970-01-04T00:00:00+00:00',
                'fields': {
                    'value': 2.50
                }
            }
        ]
        entries = json.get_sum_of_entries(body_mock)
        self.assertEqual(len(entries), 2, msg=entries)
        foo_index = 0
        bar_index = 1
        if entries[0]['measurement'] == 'sum_bar':
            foo_index = 1
            bar_index = 0
        self.assertEqual(entries[foo_index]['measurement'], 'sum_foo')
        self.assertEqual(entries[foo_index]['time'],
                         '1970-01-01T00:00:00+00:00')
        self.assertEqual(entries[foo_index]['fields']['value'], 2.50)
        self.assertEqual(entries[bar_index]['measurement'], 'sum_bar')
        self.assertEqual(entries[bar_index]['time'],
                         '1970-01-03T00:00:00+00:00')
        self.assertEqual(entries[bar_index]['fields']['value'], 4.50)

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
        self.assertEqual(len(body), 6)

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
        self.assertEqual(len(body), 6)

    @mock.patch('minflux.json.reader')
    def test_no_archive_dir(self, mock_reader):
        """Verify we don't cause errors in this mode."""
        mock_reader.TransactionReader = MockReader
        config = {
            'mint': {
                'directory': '/foo',
                'archive': None
            }
        }
        body = json.jsonify(config, '/foo/bar.csv')
        self.assertEqual(len(body), 6)


class TestJsonData(unittest.TestCase):
    """Verifies functionality of JsonData class."""

    def setUp(self):
        """Sets up the TestJsonData unit."""
        self.headers = {
            'description': 0,
            'category': 1,
            'account_name': 2,
            'labels': 3,
            'notes': 4,
            'date': 5,
            'transaction_type': 6,
            'amount': 7
        }
        self.config_no_netsum = {}
        self.config_netsum = {'net_sum': None}
        self.config_netsum_exclude = {
            'net_sum': {
                'exclude': {
                    'category': 'foobar'
                }
            }
        }
        self.test_entry = ['desc', 'cat', 'acc', 'lab',
                           'note', '1/1/1970', 'credit', '1.00']
        self.Json = json.JsonData(self.config_no_netsum, self.headers)
        self.JsonNetSum = json.JsonData(self.config_netsum, self.headers)
        self.JsonExclude = json.JsonData(self.config_netsum_exclude,
                                         self.headers)

    def tearDown(self):
        """Tears down the TestJsonData unit."""
        self.config_no_netsum = None
        self.config_netsum = None
        self.config_netsum_exclude = None
        self.Json = None
        self.JsonNetSum = None
        self.JsonExclude = None

    def test_measurement_create(self):
        """Tests the measurement creation of the JsonData class."""
        meas_category = self.Json.create_measurement(self.test_entry,
                                                     'category')
        meas_vendor = self.Json.create_measurement(self.test_entry,
                                                   'vendor')
        meas_account = self.Json.create_measurement(self.test_entry,
                                                    'account')
        self.assertEqual(meas_account, self.test_entry[2])
        self.assertEqual(meas_vendor, self.test_entry[0])
        self.assertEqual(meas_category, self.test_entry[1])

    def test_tag_create(self):
        """Tests the tag creation of the JsonData class."""
        tag_list = ['vendor', 'category', 'account']
        tag_dict = dict()
        for tag in tag_list:
            tag_dict[tag] = self.Json.create_tags(self.test_entry,
                                                  tag)
            self.assertTrue(tag not in tag_dict[tag])

    def test_netsum_logic(self):
        """Tests the logic to generate net_sum within the JsonData class."""
        self.assertTrue(self.JsonNetSum.add_net_sum_measure)
        self.assertFalse(self.JsonNetSum.check_net_sum_exclusion)
        self.assertTrue(self.JsonExclude.add_net_sum_measure)
        self.assertTrue(self.JsonExclude.check_net_sum_exclusion)
