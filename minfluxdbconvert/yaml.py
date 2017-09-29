"""Used to load and validate yaml config file."""

import os
import sys
import logging
import yaml
import voluptuous as vol
from minfluxdbconvert.util import string, ensure_list
from minfluxdbconvert.const import (CONF_HOST, CONF_PORT, CONF_USER, CONF_PASSWORD,
                                    CONF_DBNAME, CONF_FILE, CONF_LOGGER, CONF_LEVEL,
                                    CONF_INFLUX, CONF_MINT, CONF_NETSUM, CONF_EXCLUDE,
                                    CONF_VENDOR, CONF_CATEGORY, CONF_ACCOUNT, CONF_DIR,
                                    CONF_ARCHIVE)

LOGGER = logging.getLogger(__name__)

SCHEMA = vol.Schema({
    vol.Required(CONF_INFLUX): vol.Schema({
        vol.Required(CONF_HOST): string,
        vol.Required(CONF_PORT): string,
        vol.Required(CONF_USER): string,
        vol.Required(CONF_PASSWORD): string,
        vol.Required(CONF_DBNAME): string
    }),
    vol.Required(CONF_MINT): vol.Schema({
        vol.Optional(CONF_FILE): string,
        vol.Optional(CONF_DIR): string,
        vol.Optional(CONF_ARCHIVE): vol.Schema({
            vol.Optional(CONF_DIR): string
        })
    }),
    vol.Optional(CONF_LOGGER, default={CONF_FILE: '', CONF_LEVEL: 'INFO'}):
        vol.Schema({
            vol.Optional(CONF_FILE, default=''): string,
            vol.Optional(CONF_LEVEL, default=logging.INFO): string
        }),
    vol.Optional(CONF_NETSUM, default={}):
        vol.Schema({
            vol.Optional(CONF_EXCLUDE, default={}):
                vol.Schema({
                    vol.Optional(CONF_VENDOR, default=[]): ensure_list,
                    vol.Optional(CONF_CATEGORY, default=[]): ensure_list,
                    vol.Optional(CONF_ACCOUNT, default=[]): ensure_list
                })
        })
})

def load_yaml(directory):
    """Reads yaml file and returns result."""
    config_file = '{}/config.yaml'.format(directory)
    if not os.path.isfile(config_file):
        LOGGER.error('% is not a valid file', config_file)
        sys.exit(1)
    with open(config_file, 'r') as yamlfile:
        cfg = yaml.load(yamlfile)
    try:
        LOGGER.debug(SCHEMA(cfg))
        mint_props = [CONF_FILE, CONF_DIR]
        if any(x in mint_props for x in cfg[CONF_MINT]):
            return SCHEMA(cfg)
        else:
            raise vol.error.MultipleInvalid('Missing entry for mint')
    except vol.error.MultipleInvalid as err:
        LOGGER.error('Invalid configuration. %s', err)
        sys.exit(1)
            