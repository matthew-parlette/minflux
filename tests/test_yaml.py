"""Tests the yaml loading functionality."""
import unittest
from unittest import mock
from minflux import yaml as yaml


@mock.patch('minflux.yaml.os.path.isfile')
@mock.patch('minflux.yaml.yaml.load')
class TestYamlLoad(unittest.TestCase):
    """Test load_yaml functionality."""

    def test_load_min_yaml(self, mock_yaml_load, mock_isfile):
        """Tests loading of minimum required configuration."""
        config = {
            'influxdb': {
                'host': 'foo',
                'port': 1234,
                'user': 'bar',
                'password': 'foobar',
                'dbname': 'foodb'
            },
            'mint': {
                'file': 'foobar.csv'
            }
        }
        mock_isfile.return_value = True
        mock_yaml_load.return_value = config
        mock_fh = mock.mock_open()
        with mock.patch('builtins.open', mock_fh, create=False):
            x = yaml.load_yaml('/tmp')
        self.assertTrue('influxdb' in x)
        self.assertTrue('mint' in x)
        self.assertTrue('file' in x['mint'])

    def test_load_empty_yaml(self, mock_yaml_load, mock_isfile):
        """Tests loading of empty configuration."""
        config = dict()
        mock_isfile.return_value = True
        mock_yaml_load.return_value = config
        mock_fh = mock.mock_open()
        with mock.patch('builtins.open', mock_fh, create=False):
            with self.assertRaises(SystemExit) as cm:
                yaml.load_yaml('/tmp')
        self.assertEqual(cm.exception.code, 1)

    def test_load_partial_influx_config(self, mock_yaml_load, mock_isfile):
        """Tests loading of partial influxdb configuration."""
        config = {
            'influxdb': {
                'host': 'foo',
                'port': 1234,
                'user': 'bar',
                'password': 'foobar',
            },
            'mint': {
                'file': 'foobar.csv'
            }
        }
        mock_isfile.return_value = True
        mock_yaml_load.return_value = config
        mock_fh = mock.mock_open()
        with mock.patch('builtins.open', mock_fh, create=False):
            with self.assertRaises(SystemExit) as cm:
                yaml.load_yaml('/tmp')
        self.assertEqual(cm.exception.code, 1)

    def test_load_no_mint_file_config(self, mock_yaml_load, mock_isfile):
        """Tests loading of configuration missing mint."""
        config = {
            'influxdb': {
                'host': 'foo',
                'port': 1234,
                'user': 'bar',
                'password': 'foobar',
                'dbname': 'foodb'
            },
            'mint': {}
        }
        mock_isfile.return_value = True
        mock_yaml_load.return_value = config
        mock_fh = mock.mock_open()
        with mock.patch('builtins.open', mock_fh, create=False):
            with self.assertRaises(SystemExit) as cm:
                yaml.load_yaml('/tmp')
        self.assertEqual(cm.exception.code, 1)

    def test_load_logger_partial_config(self, mock_yaml_load, mock_isfile):
        """Tests loading of configuration with partial logger entry."""
        config = {
            'influxdb': {
                'host': 'foo',
                'port': 1234,
                'user': 'bar',
                'password': 'foobar',
                'dbname': 'foodb'
            },
            'mint': {
                'file': 'foobar.csv'
            },
            'logger': {
                'level': 'warning'
            }
        }
        mock_isfile.return_value = True
        mock_yaml_load.return_value = config
        mock_fh = mock.mock_open()
        with mock.patch('builtins.open', mock_fh, create=False):
            validated_config = yaml.load_yaml('/tmp')
        self.assertEqual(validated_config['logger']['file'], '')
        self.assertEqual(validated_config['logger']['level'], 'warning')

    def test_load_net_sum_config(self, mock_yaml_load, mock_isfile):
        """Tests loading of configuration with net_sum entry."""
        config = {
            'influxdb': {
                'host': 'foo',
                'port': 1234,
                'user': 'bar',
                'password': 'foobar',
                'dbname': 'foodb'
            },
            'mint': {
                'file': 'foobar.csv'
            },
            'net_sum': {
                'exclude': {
                    'account': ['test']
                }
            }
        }
        mock_isfile.return_value = True
        mock_yaml_load.return_value = config
        mock_fh = mock.mock_open()
        with mock.patch('builtins.open', mock_fh, create=False):
            validated_config = yaml.load_yaml('/tmp')
        self.assertEqual(validated_config['net_sum']['exclude']['vendor'],
                         list())
        self.assertEqual(validated_config['net_sum']['exclude']['category'],
                         list())
        self.assertEqual(validated_config['net_sum']['exclude']['account'],
                         ['test'])

    def test_file_not_exist(self, mock_yaml_load, mock_isfile):
        """Tests loading of configuration where mint file does not exist."""
        mock_isfile.return_value = False
        with self.assertRaises(SystemExit) as cm:
            yaml.load_yaml('/tmp/doesnotexist')
        self.assertEqual(cm.exception.code, 1)

    def test_min_dir_only(self, mock_yaml_load, mock_isfile):
        """Tests loading of minimum configuration with directory specified."""
        config = {
            'influxdb': {
                'host': 'foo',
                'port': 1234,
                'user': 'bar',
                'password': 'foobar',
                'dbname': 'foodb'
            },
            'mint': {
                'directory': '/foo/bar'
            }
        }
        mock_isfile.return_value = True
        mock_yaml_load.return_value = config
        mock_fh = mock.mock_open()
        with mock.patch('builtins.open', mock_fh, create=False):
            x = yaml.load_yaml('/tmp')
        self.assertTrue('directory' in x['mint'])

    def test_config_archive(self, mock_yaml_load, mock_isfile):
        """Tests loading of configuration where archive requested."""
        config = {
            'influxdb': {
                'host': 'foo',
                'port': 1234,
                'user': 'bar',
                'password': 'foobar',
                'dbname': 'foodb'
            },
            'mint': {
                'file': 'foobar.csv',
                'archive': None
            }
        }
        mock_isfile.return_value = True
        mock_yaml_load.return_value = config
        mock_fh = mock.mock_open()
        with mock.patch('builtins.open', mock_fh, create=False):
            x = yaml.load_yaml('/tmp')
        self.assertTrue('influxdb' in x)
        self.assertTrue('mint' in x)
        self.assertTrue('file' in x['mint'])
        self.assertTrue('archive' in x['mint'])

    def test_config_archive_with_dir(self, mock_yaml_load, mock_isfile):
        """Tests configuration load where archive directory requested."""
        config = {
            'influxdb': {
                'host': 'foo',
                'port': 1234,
                'user': 'bar',
                'password': 'foobar',
                'dbname': 'foodb'
            },
            'mint': {
                'file': 'foobar.csv',
                'archive': {
                    'directory': '/tmp'
                }
            }
        }
        mock_isfile.return_value = True
        mock_yaml_load.return_value = config
        mock_fh = mock.mock_open()
        with mock.patch('builtins.open', mock_fh, create=False):
            x = yaml.load_yaml('/tmp')
        self.assertTrue('influxdb' in x)
        self.assertTrue('mint' in x)
        self.assertTrue('file' in x['mint'])
        self.assertTrue('archive' in x['mint'])
        self.assertEqual('/tmp', x['mint']['archive']['directory'])
