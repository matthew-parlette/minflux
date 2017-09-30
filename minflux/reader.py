"""Module used to read csv and report results."""
import os
import sys
import pathlib
import shutil
import gzip
import csv
import logging
from minflux.const import (ATTR_DATE, ATTR_DESC, ATTR_LABELS,
                           ATTR_NOTES, ATTR_ACCOUNT, ATTR_CATEGORY,
                           ATTR_TYPE, ATTR_AMOUNT)

LOGGER = logging.getLogger(__name__)


class TransactionReader(object):
    """Class to parse transactions."""

    def __init__(self, csvfile, archive=False, archive_dir=None):
        """Initialize class."""
        self._csvfile = csvfile
        self._data = None
        if not os.path.isfile(self._csvfile):
            LOGGER.error("Invalid file %s", self._csvfile)
            sys.exit(1)
        self.read_csv()
        self._headers = {
            ATTR_DATE: None,
            ATTR_DESC: None,
            ATTR_LABELS: None,
            ATTR_NOTES: None,
            ATTR_ACCOUNT: None,
            ATTR_CATEGORY: None,
            ATTR_AMOUNT: None,
            ATTR_TYPE: None
        }
        self.get_headers()
        if archive:
            self.archive(archive_dir)

    @property
    def headers(self):
        """Returns header index dict."""
        return self._headers

    @property
    def data(self):
        """Returns data read in from csv file."""
        return self._data

    def read_csv(self):
        """Reads the csv file."""
        data = list()
        with open(self._csvfile, newline='') as txfile:
            txreader = csv.reader(txfile, delimiter=',', quotechar='"')
            for row in txreader:
                data.append(row)
        self._data = data

    def get_headers(self):
        """Retrieve header data from csv input."""
        header_line = self._data[0]
        for item in header_line:
            LOGGER.debug(item)
            key = item.lower()
            key = key.replace(' ', '_')
            self._headers[key] = header_line.index(item)

        LOGGER.debug("Headers: %s", self._headers)
        # Get rid of header line from data
        self._data.pop(0)

    def archive(self, archive_dir):
        """Used to send csv file to archive."""
        current_path = pathlib.Path(self._csvfile)
        if not archive_dir:
            archive_dir = '{}/archive'.format(current_path.parent)
        # Creates directory if it does not exist
        pathlib.Path(archive_dir).mkdir(parents=True, exist_ok=True)
        file_name_only = current_path.name
        check_file = '{}/{}.gzip'.format(archive_dir, file_name_only)

        # Make sure there are no name collisions with archive
        if os.path.exists(check_file):
            file_name_no_ext = current_path.stem
            count = 1
            check_file = '{}/{}_{}.csv.gzip'.format(archive_dir,
                                                    file_name_no_ext,
                                                    count)
            while os.path.exists(check_file):
                count += 1
                check_file = '{}/{}_{}.csv.gzip'.format(archive_dir,
                                                        file_name_no_ext,
                                                        count)
                if count > 256:
                    LOGGER.error("Too many name collisions during "
                                 "archive of %s.  Consider using files "
                                 "with unique names instead.",
                                 file_name_no_ext)
                    sys.exit(1)
        LOGGER.info("Compressing with gzip to %s", check_file)
        with gzip.GzipFile(check_file, 'wb') as gzipfile:
            with open(self._csvfile, 'rb') as input_file:
                shutil.copyfileobj(input_file, gzipfile)
