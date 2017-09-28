"""Primary module for minfluxdb-convert."""
import sys
import json
import os
import logging
from influxdb import InfluxDBClient
import minfluxdbconvert.util as util
import minfluxdbconvert.reader as reader
from minfluxdbconvert.yaml import load_yaml
from minfluxdbconvert.const import (ATTR_DATE, ATTR_DESC, ATTR_LABELS, ATTR_NOTES,
                                    ATTR_ACCOUNT, ATTR_CATEGORY, ATTR_TYPE, ATTR_AMOUNT)
from minfluxdbconvert.const import (CONF_INFLUX, CONF_USER, CONF_PASSWORD, CONF_DBNAME,
                                    CONF_HOST, CONF_PORT, CONF_FILE, CONF_MINT, CONF_LOGGER,
                                    CONF_LEVEL)
from minfluxdbconvert.const import (ARG_CONFIG, ARG_NOPUSH)

LOGGER = logging.getLogger(__name__)

def create_json_file(config, csvfile):
    """Converts csv from mint into json file."""
    Mint = reader.TransactionReader(csvfile)
    json_body = list()
    for entry in Mint.data:
        value = util.convert_value(entry[Mint.headers[ATTR_AMOUNT]],
                                   entry[Mint.headers[ATTR_TYPE]])
        json_entry = {'measurement': entry[Mint.headers[ATTR_CATEGORY]],
                      'tags': {
                          'vendor': entry[Mint.headers[ATTR_DESC]],
                          'label': entry[Mint.headers[ATTR_LABELS]],
                          'notes': entry[Mint.headers[ATTR_NOTES]],
                          'account': entry[Mint.headers[ATTR_ACCOUNT]],
                          },
                      'time': util.date_to_epoch(entry[Mint.headers[ATTR_DATE]]),
                      'fields': {
                          'value': value
                          }
                      }
        json_body.append(json_entry)
    return json_body

def get_arguments():
    """Gets command line arguments."""
    opts = dict()
    parser = util.Parser()
    for arg in vars(parser.args):
        opts[arg] = getattr(parser.args, arg)
    return opts

def main():
    """Start conversion."""
    args = get_arguments()
    config = load_yaml(args[ARG_CONFIG])
    util.set_loggers(LOGGER, file=config[CONF_LOGGER][CONF_FILE], level=config[CONF_LOGGER][CONF_LEVEL])

    source_file = config[CONF_MINT][CONF_FILE]

    json_body = create_json_file(config, source_file)
    LOGGER.debug(json_body)
    if args[ARG_NOPUSH]:
        LOGGER.warn('Skipping database write.')
        json_info = json.dumps(json_body)
        with open('dump.json', 'w') as outfile:
            json.dump(json_info, outfile)
        LOGGER.info('Data sent to {}/dump.json'.format(os.getcwd()))
        sys.exit()
    else:
        host = config[CONF_INFLUX][CONF_HOST]
        port = config[CONF_INFLUX][CONF_PORT]
        db = config[CONF_INFLUX][CONF_DBNAME]
        user = config[CONF_INFLUX][CONF_USER]
        password = config[CONF_INFLUX][CONF_PASSWORD]

        client = InfluxDBClient(host, port, user, password, dbname)
        client.write_points(json_body)

    LOGGER.info('Databse write successful! :)')
    sys.exit()


if __name__ == "__main__":
    
    main()
