"""Tests the util functionality."""
import unittest
import voluptuous as vol
import logging
from minflux import util as util


class TestUtilFunctions(unittest.TestCase):
    """Test util functionality."""

    def test_date_to_iso(self):
        """Tests date to iso standard."""
        date = '1/8/1970'
        self.assertEqual(util.date_to_iso(date),
                         '1970-01-08T00:00:00+00:00')
        self.assertEqual(util.date_to_iso(date, month_only=True),
                         '1970-01-01T00:00:00+00:00')

    def test_convert_value(self):
        """Tests conversion of value to signed value."""
        self.assertEqual(util.convert_value(10, 'debit'), -10)
        self.assertEqual(util.convert_value(10, 'credit'), 10)

    def test_string(self):
        """Tests string assertion."""
        self.assertEqual(util.string(1234), '1234')
        self.assertEqual(util.string(True), 'True')

    def test_invalid_string(self):
        """Tests string assertion with invalid value."""
        with self.assertRaises(vol.Invalid):
            util.string(None)

    def test_boolean(self):
        """Tests boolean assertion."""
        for bool_val in ['1', 'True', 'yes', 'ON', 'enable']:
            self.assertTrue(util.boolean(bool_val))
        for bool_val in ['0', 'false', 'NO', 'off', 'disable']:
            self.assertFalse(util.boolean(bool_val))

    def test_invalid_boolean(self):
        """Tests boolean assertion with invalid value."""
        with self.assertRaises(vol.Invalid):
            util.boolean('foobar')

    def test_logger_setup(self):
        """Tests logger setup."""
        logger = logging.getLogger('dummy_test')
        util.set_loggers(logger, file=None, level='dEbUg')
        util.set_loggers(logger, file=None, level='ERROR')
