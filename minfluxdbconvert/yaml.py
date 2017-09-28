"""Used to load and validate yaml config file."""
import logging
import coloredlogs
import yaml
import os
import sys
import voluptuous as vol
from minfluxdbconvert.util import string
from minfluxdbconvert.const import (CONF_HOST, CONF_PORT, CONF_USER, CONF_PASSWORD,
                                    CONF_DBNAME, CONF_FILE, CONF_LOGGER, CONF_LEVEL,
                                    CONF_INFLUX, CONF_MINT)

LOGGER = logging.getLogger(__name__)

SCHEMA = vol.Schema({
    CONF_INFLUX: vol.Schema({
        vol.Required(CONF_HOST): string,
        vol.Required(CONF_PORT): string,
        vol.Required(CONF_USER): string,
        vol.Required(CONF_PASSWORD): string,
        vol.Required(CONF_DBNAME): string
    }),
    CONF_MINT: vol.Schema({
        vol.Required(CONF_FILE): string
    }),
    vol.Optional(CONF_LOGGER, default={CONF_FILE: '', CONF_LEVEL: 'INFO'}):
        vol.Schema({
            vol.Optional(CONF_FILE, default=''): string,
            vol.Optional(CONF_LEVEL, default=logging.INFO): string
        })
})

def load_yaml(directory):
    """Reads yaml file and returns result."""
    config_file = '{}/config.yaml'.format(directory)
    if not os.path.isfile(config_file):
        LOGGER.error('{} is not a valid file'.format(config_file))
        sys.exit(1)
    with open(config_file, 'r') as yamlfile:
        cfg = yaml.load(yamlfile)
    try:
        LOGGER.debug(SCHEMA(cfg))
        return(SCHEMA(cfg))
    except vol.error.MultipleInvalid as e:
        LOGGER.error('Invalid configuration. {}'.format(e))
        sys.exit(1)
            