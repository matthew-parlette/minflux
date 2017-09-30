"""Tests dbwrite functionality."""
import unittest
from unittest import mock
from minflux import dbwrite as dbwrite


class TestInfluxClient(unittest.TestCase):
    """Tests InfluxClient class."""

    def setUp(self):
        """General initialization."""
        self.config = {
            'influxdb': {
                'host': 'foo',
                'port': 1234,
                'dbname': 'foobar',
                'user': 'bar',
                'password': 'barfoo'
            }
        }

    def tearDown(self):
        """Tear down routine called after each test."""
        self.config = dict()

    def test_init(self):
        """Tests initialization of InfluxClient."""
        client = dbwrite.InfluxClient(self.config)
        self.assertEqual(client.host, self.config['influxdb']['host'])
        self.assertEqual(client.port, self.config['influxdb']['port'])
        self.assertEqual(client.dbname, self.config['influxdb']['dbname'])
        self.assertEqual(client.user, self.config['influxdb']['user'])
        self.assertEqual(client.password, self.config['influxdb']['password'])

    @mock.patch('minflux.dbwrite.InfluxDBClient.write_points')
    def test_write_data(self, mock_influx):
        """Tests the write_data call inside InfluxClient."""
        mock_influx.return_value = None
        client = dbwrite.InfluxClient(self.config)
        client.write_data('')
        self.assertEqual(mock_influx.call_count, 1)


class TestInfluxDBWriter(unittest.TestCase):
    """Class tests functionality of influxdb_write."""

    def setUp(self):
        """General initialization."""
        self.config = {
            'influxdb': {
                'host': 'foo',
                'port': 1234,
                'dbname': 'foobar',
                'user': 'bar',
                'password': 'barfoo'
            }
        }
        self.client = dbwrite.InfluxClient(self.config)

    def tearDown(self):
        """Tear down routine called after each test."""
        self.config = dict()
        self.client = None

    @mock.patch('minflux.dbwrite.json.dump')
    @mock.patch('minflux.dbwrite.jsonify')
    def test_db_skip(self, mock_json, mock_jsonify):
        """Tests return of db_skip."""
        mock_json.return_value = True
        mock_jsonify.return_value = {}
        self.assertTrue(dbwrite.influxdb_write(self.config,
                                               self.client,
                                               '',
                                               db_skip=True))

    @mock.patch('minflux.dbwrite.jsonify')
    @mock.patch('minflux.dbwrite.InfluxDBClient.write_points')
    def test_normal_write(self, mock_influx, mock_jsonify):
        """Tests a normal db write."""
        mock_influx.return_value = None
        mock_jsonify.return_value = dict()
        self.assertTrue(dbwrite.influxdb_write(self.config, self.client, ''))
        self.assertEqual(mock_influx.call_count, 1)
