"""Module that handles writing to database."""
import logging
import json
from influxdb import InfluxDBClient
from minfluxdbconvert.json import jsonify
from minfluxdbconvert.const import (CONF_INFLUX, CONF_HOST, CONF_PORT,
                                    CONF_USER, CONF_PASSWORD, CONF_DBNAME)

LOGGER = logging.getLogger(__name__)


def influxdb_write(config, client, source, db_skip=False):
    """Reads source data and writes to client."""
    json_body = jsonify(config, source)
    if db_skip:
        LOGGER.warning("Skipping database write.")
        json_info = json.dumps(json_body)
        with open('{}.json'.format(source), 'w') as outfile:
            json.dump(json_info, outfile)
        LOGGER.info("Data sent to %s.json", source)
        return True

    client.write_data(json_body)

    return True


class InfluxClient(object):
    """Wrapper class for influx client."""

    def __init__(self, config):
        """Initialize the InfluxDB Client."""
        self.host = config[CONF_INFLUX][CONF_HOST]
        self.port = config[CONF_INFLUX][CONF_PORT]
        self.dbname = config[CONF_INFLUX][CONF_DBNAME]
        self.user = config[CONF_INFLUX][CONF_USER]
        self.password = config[CONF_INFLUX][CONF_PASSWORD]
        self.client = InfluxDBClient(self.host,
                                     self.port,
                                     self.user,
                                     self.password,
                                     self.dbname)

    def write_data(self, data):
        """Wrapper for influxdb writes."""
        LOGGER.debug("Writing to %s as %s: %s", self.dbname, self.user, data)
        self.client.write_points(data)
