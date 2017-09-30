"""Various helper functions for minfluxdb-convert."""
import logging
import argparse
from typing import Any, Union, TypeVar, Sequence
from datetime import datetime
import coloredlogs
import voluptuous as vol
import pytz
from minfluxdbconvert.const import (ARG_CONFIG, ARG_NOPUSH)

# typing typevar
T = TypeVar('T')

LOGGER = logging.getLogger(__name__)


def date_to_iso(date):
    """Converts timestamp to ISO 8601."""
    dtobj = pytz.utc.localize(datetime.strptime(date, '%m/%d/%Y'))
    return dtobj.isoformat()


def convert_value(value, txtype):
    """Converts value to +/- based on credit/debit transaction type."""
    txtype_map = {'credit': 1, 'debit': -1}
    LOGGER.debug("Found amount %s of type %s", value, txtype)
    return round(txtype_map[txtype] * float(value), 2)


def set_loggers(logger, file=None, level='info'):
    """Sets up loggers."""
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    level = level.lower()
    level_dict = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warn': logging.WARNING,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }
    if file:
        handler = logging.FileHandler(file)
        handler.setLevel(level_dict[level])
        formatter = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        handler.setFormatter(logging.Formatter(formatter))
        root.addHandler(handler)

    coloredlogs.install(level=level.upper())


def string(value: Any) -> str:
    """Force value to string if not None."""
    if value is not None:
        return str(value)
    raise vol.Invalid("string value is None")


def boolean(value: Any) -> bool:
    """Validate and coerce a boolean value."""
    if isinstance(value, str):
        value = value.lower()
        if value in ('1', 'true', 'yes', 'on', 'enable'):
            return True
        if value in ('0', 'false', 'no', 'off', 'disable'):
            return False
        raise vol.Invalid("invalid boolean value {}".format(value))
    return bool(value)


def ensure_list(value: Union[T, Sequence[T]]) -> Sequence[T]:
    """Wrap value in list if it is not one."""
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


class Parser(object):
    """Argument parsing class."""

    def __init__(self):
        """Intialize arguments for parser."""
        self.parser = argparse.ArgumentParser(__name__)
        self.add_args()

    def add_args(self):
        """Adds arguments."""
        self.parser.add_argument(
            '--{}'.format(ARG_CONFIG.replace('_', '-')),
            help="Directory of db config file.",
            type=str,
            required=True
        )
        self.parser.add_argument(
            '--{}'.format(ARG_NOPUSH.replace('_', '-')),
            help="Only generate data file without pushing to db.",
            action='store_true'
        )

    @property
    def args(self):
        """Return list of args."""
        return self.parser.parse_args()
