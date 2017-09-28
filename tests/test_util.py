"""Tests the util functionality."""
import unittest
from unittest import mock
import voluptuous as vol
from minfluxdbconvert import util as util

class TestUtilFunctions(unittest.TestCase):
    """Test util functionality."""
    
    def test_date_to_epoch(self):
        date = '1/1/1970'
        self.assertEqual(util.date_to_epoch(date), '1970-01-01T00:00:00+00:00')
 
    def test_convert_value(self):
        self.assertEqual(util.convert_value(10, 'debit'), -10)
        self.assertEqual(util.convert_value(10, 'credit'), 10)

    def test_string(self):
        self.assertEqual(util.string(1234), '1234')
        self.assertEqual(util.string(True), 'True')
    
    def test_invalid_string(self):
        with self.assertRaises(vol.Invalid):
            util.string(None)

    def test_boolean(self):
        for bool_val in ['1', 'True', 'yes', 'ON', 'enable']:
            self.assertTrue(util.boolean(bool_val))
        for bool_val in ['0', 'false', 'NO','off', 'disable']:
            self.assertFalse(util.boolean(bool_val))

    def test_invalid_boolean(self):
        with self.assertRaises(vol.Invalid):
            util.boolean('foobar')
