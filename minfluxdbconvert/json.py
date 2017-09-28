import sys
import json
import os
import logging
import minfluxdbconvert.reader as reader
import minfluxdbconvert.util as util
from minfluxdbconvert.const import (ATTR_DATE, ATTR_DESC, ATTR_LABELS, ATTR_NOTES,
                                    ATTR_ACCOUNT, ATTR_CATEGORY, ATTR_TYPE, ATTR_AMOUNT)
from minfluxdbconvert.const import (CONF_NETSUM, CONF_EXCLUDE, CONF_VENDOR, CONF_CATEGORY, CONF_ACCOUNT)
                                    
LOGGER = logging.getLogger(__name__)

def jsonify(config, csvfile):
    """Converts csv from mint into json file."""
    Mint = reader.TransactionReader(csvfile)
    headers = Mint.headers
    json_body = list()
    all_dates = list()
    net_value = 0
    for entry in Mint.data:
        value = util.convert_value(entry[headers[ATTR_AMOUNT]],
                                   entry[headers[ATTR_TYPE]])
        date = util.date_to_epoch(entry[headers[ATTR_DATE]])
        all_dates.append(date)
        json_entry = {'tags': {
                        'label': entry[headers[ATTR_LABELS]],
                        'notes': entry[headers[ATTR_LABELS]],
                        },
                      'time': date,
                      'fields': {
                          'value': value
                          }
                      }
        
        json_body.append(sort_by_category(json_entry, entry, headers))
        json_body.append(sort_by_vendor(json_entry, entry, headers))
        json_body.append(sort_by_account(json_entry, entry, headers))
        if CONF_NETSUM in config and CONF_EXCLUDE in config[CONF_NETSUM]:
            net_value += check_entry_for_net_sum(config[CONF_NETSUM], entry, headers, value)
        
    json_body.append(net_sum_entry(net_value, all_dates))
    return json_body

def net_sum_entry(net_value, all_dates):
    """Creates entry for net summation across measurements."""
    json_entry = {'measurement': CONF_NETSUM,
                  'time': min(all_dates),
                  'fields': {
                      'value': net_value
                      }
                 }
    return json_entry
    
def sort_by_category(json_entry, entry, headers):
    """Creates structure with category as measurement."""
    json_entry['measurement'] = entry[headers[ATTR_CATEGORY]]
    json_entry['tags']['vendor'] = entry[headers[ATTR_DESC]]
    json_entry['tags']['account'] = entry[headers[ATTR_ACCOUNT]]
    return json_entry

def sort_by_vendor(json_entry, entry, headers):
    """Creates structure with vendor as measurement."""
    json_entry['measurement'] = entry[headers[ATTR_DESC]]
    json_entry['tags']['category'] = entry[headers[ATTR_CATEGORY]]
    json_entry['tags']['account'] = entry[headers[ATTR_ACCOUNT]]
    return json_entry
    
def sort_by_account(json_entry, entry, headers):
    """Creates structure with vendor as measurement."""
    json_entry['measurement'] = entry[headers[ATTR_ACCOUNT]]
    json_entry['tags']['vendor'] = entry[headers[ATTR_DESC]]
    json_entry['tags']['category'] = entry[headers[ATTR_CATEGORY]]
    return json_entry

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
    
    
    