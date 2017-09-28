"""
Various helper functions for minfluxdb-convert.
"""
import sys
import argparse
import yaml
from datetime import datetime


def load_yaml(filename):
    """Reads yaml file and returns result."""
    with open(filename, 'r') as yamlfile:
        cfg = yaml.load(yamlfile)
    return cfg

def date_to_epoch(date):
    """Converts timestamp to epoch ns."""
    dtobj = datetime.strptime(date, '%m/%d/%Y')

    return round(dtobj.timestamp() * 1e9)

def convert_value(value, txtype):
    """Converts value to +/- based on credit/debit transaction type."""
    txtype_map = {'credit': 1, 'debit': -1}
    return round(txtype_map[txtype] * float(value), 2)

class Parser(object):
    """Argument parsing class."""

    def __init__(self):
        """Intialize arguments for parser."""
        self.parser = argparse.ArgumentParser(__name__)
        self.add_args()

    def add_args(self):
        """Adds arguments."""
        self.parser.add_argument('--db-cfg',
                                 help='Location of db config file.',
                                 type=str,
                                 required=False,
                                 default='./db.yaml'
                                 )
        self.parser.add_argument('--skip-push',
                                 help='Only generate data file without pushing to db.',
                                 action='store_true'
                                 )

    @property
    def args(self):
        """Return list of args."""
        return self.parser.parse_args()
