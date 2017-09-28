"""Primary module for minfluxdb-convert."""
import sys
import json
import os
import logging
from influxdb import InfluxDBClient
import minfluxdbconvert.util as util
import minfluxdbconvert.reader as reader
import minfluxdbconvert.yaml as yaml
from minfluxdbconvert.json import jsonify
from minfluxdbconvert.const import (CONF_INFLUX, CONF_USER, CONF_PASSWORD, CONF_DBNAME,
                                    CONF_HOST, CONF_PORT, CONF_FILE, CONF_MINT, CONF_LOGGER,
                                    CONF_LEVEL)
from minfluxdbconvert.const import (ARG_CONFIG, ARG_NOPUSH)

LOGGER = logging.getLogger(__name__)

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
    config = yaml.load_yaml(args[ARG_CONFIG])
    util.set_loggers(LOGGER, file=config[CONF_LOGGER][CONF_FILE], level=config[CONF_LOGGER][CONF_LEVEL])

    source_file = config[CONF_MINT][CONF_FILE]

    json_body = jsonify(config, source_file)
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

        client = InfluxDBClient(host, port, user, password, db)
        client.write_points(json_body)

    LOGGER.info('Databse write successful! :)')
    sys.exit()


if __name__ == "__main__":
    main()
