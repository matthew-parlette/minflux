"""Module used to read csv and report results."""

import csv
import logging
from minfluxdbconvert.const import (ATTR_DATE, ATTR_DESC, ATTR_LABELS, ATTR_NOTES,
                                    ATTR_ACCOUNT, ATTR_CATEGORY, ATTR_TYPE, ATTR_AMOUNT)

LOGGER = logging.getLogger(__name__)
                                    
class TransactionReader(object):
    """Class to parse transactions."""

    def __init__(self, csvfile):
        """Initialize class."""
        self._data = self.read_csv(csvfile)
        self._headers = {ATTR_DATE: None,
                         ATTR_DESC: None,
                         ATTR_LABELS: None,
                         ATTR_NOTES: None,
                         ATTR_ACCOUNT: None,
                         ATTR_CATEGORY: None,
                         ATTR_AMOUNT: None,
                         ATTR_TYPE: None
                         }
        self.get_headers()

    @property
    def headers(self):
        return self._headers

    @property
    def data(self):
        return self._data

    def read_csv(self, csvfile):
        """Reads the csv file."""
        data = list()
        with open(csvfile, newline='') as txfile:
            txreader = csv.reader(txfile, delimiter=',', quotechar='"')
            for row in txreader:
                data.append(row)
        return data

    def get_headers(self):
        """Retrieve header data from csv input."""
        header_line = self._data[0]
        for item in header_line:
            LOGGER.debug(item)
            key = item.lower()
            key = key.replace(' ', '_')
            self._headers[key] = header_line.index(item)
        LOGGER.debug('Headers: {}'.format(self._headers))
        # Get rid of header line from data
        self._data.pop(0)


