"""Tests the json building functionality."""
import unittest
from unittest import mock
from minfluxdbconvert import json as json

class MockReader(object):
    """Class used to mock the reader module."""
    def __init__(self, file):
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
        self.data = [['1/1/1970', 'foo', 'bar', 'credit', '3.50', 'foocat', 'foolabel', 'barnote'],
                     ['1/2/1970', 'oof', 'rab', 'debit', '1.25', 'tacoof', 'lebaloof', 'etonrab']]

class TestYamlLoad(unittest.TestCase):
    """Test jsonify functionality."""
    
    def setUp(self):
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
        pass
    
    def test_sort_by_category(self):
        json_expected = {
            'measurement': 'foo',
            'tags': {
                'vendor': 'bar',
                'account': 'foobar'
            }
        }
        
        self.assertEqual(json.sort_by_category(self.json, self.entry, self.headers),
                         json_expected)

    def test_sort_by_vendor(self):
        json_expected = {
            'measurement': 'bar',
            'tags': {
                'category': 'foo',
                'account': 'foobar'
            }
        }
        
        self.assertEqual(json.sort_by_vendor(self.json, self.entry, self.headers),
                         json_expected)

    def test_sort_by_account(self):
        json_expected = {
            'measurement': 'foobar',
            'tags': {
                'vendor': 'bar',
                'category': 'foo'
            }
        }
        
        self.assertEqual(json.sort_by_account(self.json, self.entry, self.headers),
                         json_expected)

    def test_net_sum_no_exclude(self):
        value = 0
        value += json.check_entry_for_net_sum(self.netsum_config, self.entry, self.headers, 1)
        value += json.check_entry_for_net_sum(self.netsum_config, self.entry_2, self.headers, 3)
        self.assertEqual(value, 4)

    def test_net_sum_with_exclude(self):
        value = 0
        self.netsum_config['exclude']['vendor'] = ['bar']
        value += json.check_entry_for_net_sum(self.netsum_config, self.entry, self.headers, 1)
        value += json.check_entry_for_net_sum(self.netsum_config, self.entry_2, self.headers, 3)
        self.assertEqual(value, 3, msg='{}'.format(self.netsum_config))

    def test_netsum_json_entry(self):
        all_dates = [
            '1970-01-01T00:00:00+00:00',
            '1970-01-02T00:00:00+00:00',
            '1970-01-03T00:00:00+00:00'
        ]
        returned_entry = json.net_sum_entry(5, all_dates)
        self.assertEqual(returned_entry['time'], all_dates[0])
        self.assertEqual(returned_entry['fields']['value'], 5)
        self.assertEqual(returned_entry['measurement'], 'net_sum')
    
    @mock.patch('minfluxdbconvert.json.reader')
    def test_jsonify(self, mock_reader):
        mock_reader.TransactionReader = MockReader
        body = json.jsonify({'net_sum': self.netsum_config}, '/tmp/notreal')
        self.assertEqual(len(body), 7)
        self.assertEqual(body[-1]['measurement'], 'net_sum')
        self.assertEqual(body[-1]['fields']['value'], 2.25)        
