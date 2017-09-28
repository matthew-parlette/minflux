"""Module used to read csv and report results."""

import csv

class TransactionReader(object):
    """Class to parse transactions."""

    def __init__(self, csvfile):
        """Initialize class."""
        self._data = self.read_csv(csvfile)
        self._headers = {'Date': None,
                         'Description': None,
                         'Labels': None,
                         'Notes': None,
                         'Account Name': None,
                         'Category': None,
                         'Amount': None,
                         'Transaction Type': None
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
            txreader = csv.reader(txfile, delimiter=',', quotechar='\"')
            for row in txreader:
                data.append(row)
        return data

    def get_headers(self):
        """Retrieve header data from csv input."""
        header_line = self._data[0]
        for key in self._headers:
            self._headers[key] = header_line.index(key)
        # Get rid of header line from data
        self._data.pop(0)


