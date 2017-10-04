"""Module used to create influxdb json data."""

import logging
import minflux.reader as reader
import minflux.util as util
from minflux.const import (ATTR_DATE, ATTR_DESC, ATTR_LABELS,
                           ATTR_NOTES, ATTR_ACCOUNT, ATTR_CATEGORY,
                           ATTR_TYPE, ATTR_AMOUNT)
from minflux.const import (CONF_NETSUM, CONF_EXCLUDE, CONF_VENDOR,
                           CONF_CATEGORY, CONF_ACCOUNT, CONF_MINT,
                           CONF_DIR, CONF_ARCHIVE, CONF_SUM)

LOGGER = logging.getLogger(__name__)


class JsonData(object):
    """Representation of json data for InfluxDB."""

    def __init__(self, config, headers):
        """Initialize the Jsonjson_data class."""
        self.headers = headers
        self.body = list()
        self.all_dates = list()
        self.net_value = 0
        self.add_net_sum_measure = False
        self.check_net_sum_exclusion = False
        self.measure_map = {
            'vendor': ATTR_DESC,
            'category': ATTR_CATEGORY,
            'account': ATTR_ACCOUNT
        }
        self.json_entry = {
            'tags': {
                'label': None,
                'notes': None,
            },
            'time': None,
        }
        if CONF_NETSUM in config:
            self.add_net_sum_measure = True
            if (config[CONF_NETSUM] is not None and
                    CONF_EXCLUDE in config[CONF_NETSUM]):
                self.check_net_sum_exclusion = True

    def create_measurement(self, entry, measure_type):
        """Returns measurement name for measure_type."""
        return entry[self.headers[self.measure_map[measure_type]]]

    def create_tags(self, entry, measurement):
        """Removes 'measurement' from normal tag list."""
        tag_dict = {
            'vendor': entry[self.headers[ATTR_DESC]],
            'category': entry[self.headers[ATTR_CATEGORY]],
            'account': entry[self.headers[ATTR_ACCOUNT]],
            'raw_date': entry[self.headers[ATTR_DATE]],
            'label': entry[self.headers[ATTR_LABELS]],
            'notes': entry[self.headers[ATTR_NOTES]],
        }
        tag_dict.pop(measurement, None)

        return tag_dict

    def create_entry(self, entry, date):
        """Creates a generic json data set."""
        self.json_entry['time'] = date

    def create_value_entry(self, value_dict):
        """Adds a custom field to data."""
        self.json_entry['fields'] = value_dict

    def append_net_sum_entry(self):
        """Appends a net_sum entry to the end of the json body."""
        json_entry = {
            'measurement': CONF_NETSUM,
            'time': min(self.all_dates),
            'fields': {
                'value': self.net_value
            }
        }
        self.body.append(json_entry)


def jsonify(config, csvfile):
    """Converts csv from mint into json file."""
    try:
        arch_config = config[CONF_MINT][CONF_ARCHIVE]
        arch_dir = None
        if arch_dir is not None and CONF_DIR in arch_config:
            arch_dir = arch_config[CONF_DIR]
        mint = reader.TransactionReader(csvfile,
                                        archive=True,
                                        archive_dir=arch_dir)
    except KeyError:
        mint = reader.TransactionReader(csvfile)

    json_data = JsonData(config, mint.headers)

    for entry in mint.data:
        value_dict = dict()
        value = util.convert_value(entry[json_data.headers[ATTR_AMOUNT]],
                                   entry[json_data.headers[ATTR_TYPE]])
        date = util.date_to_iso(entry[json_data.headers[ATTR_DATE]])
        value_dict['value'] = value
        json_data.all_dates.append(date)

        json_data.create_entry(entry, date)

        for measurement in ['category', 'vendor', 'account']:
            measure_name = json_data.create_measurement(entry, measurement)
            json_data.json_entry['measurement'] = measure_name
            tag_dict = json_data.create_tags(entry, measurement)
            json_data.json_entry['tags'] = tag_dict
            LOGGER.debug("Generating data for %s", measure_name)
            json_data.create_value_entry(value_dict)
            json_data.body.append(json_data.json_entry.copy())

        if CONF_NETSUM in config and CONF_EXCLUDE in config[CONF_NETSUM]:
            json_data.net_value += check_entry_for_net_sum(config[CONF_NETSUM],
                                                           entry,
                                                           json_data.headers,
                                                           value)
        elif CONF_NETSUM in config:
            json_data.net_value += value

    if CONF_NETSUM in config:
        json_data.append_net_sum_entry()

    if CONF_SUM in config[CONF_MINT]:
        for entry in get_sum_of_entries(json_data.body):
            json_data.body.append(entry)

    return json_data.body


def check_entry_for_net_sum(config, entry, headers, value):
    """Checks if entry is valid for summing."""
    vendor = entry[headers[ATTR_DESC]]
    category = entry[headers[ATTR_CATEGORY]]
    account = entry[headers[ATTR_ACCOUNT]]

    if (vendor not in config[CONF_EXCLUDE][CONF_VENDOR] and
            category not in config[CONF_EXCLUDE][CONF_CATEGORY] and
            account not in config[CONF_EXCLUDE][CONF_ACCOUNT]):
        return value
    return 0


def get_sum_of_entries(body):
    """Find all measurements and sum across them."""
    all_measures = dict()
    for entry in body:
        key = entry['measurement']
        if key not in all_measures:
            all_measures[key] = list()
        try:
            value = [
                entry['tags']['raw_date'],
                entry['fields']['value']
            ]
            all_measures[key].append(value)
        except KeyError:
            pass
    new_entries = []
    for key, entries in all_measures.items():
        val = 0
        LOGGER.debug("%s", entries)
        for entry in entries:
            iso_date = util.date_to_iso(entry[0], month_only=True)
            val += entry[1]
        entry_name = 'sum_{}'.format(key)
        LOGGER.debug("Creating %s", entry_name)
        sum_entry = {
            'measurement': entry_name,
            'time': iso_date,
            'fields': {
                'value': val
            }
        }
        new_entries.append(sum_entry)
    return new_entries
