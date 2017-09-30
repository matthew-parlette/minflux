"""Primary module for minflux."""
import sys
import glob
import logging
import argparse
import minflux.util as util
import minflux.yaml as yaml
import minflux.dbwrite as dbwrite
from minflux.const import (CONF_FILE, CONF_MINT, CONF_LOGGER,
                           CONF_LEVEL, CONF_DIR)
from minflux.const import (__version__, ARG_CONFIG, ARG_NOPUSH)

LOGGER = logging.getLogger(__name__)


class Parser(object):
    """Argument parsing class."""

    def __init__(self):
        """Intialize arguments for parser."""
        self.parser = argparse.ArgumentParser(__name__)
        self.add_args()

    def add_args(self):
        """Adds arguments."""
        self.parser.add_argument(
            '--{}'.format(ARG_CONFIG.replace('_', '-')),
            help="Directory of db config file.",
            type=str,
            required=True
        )
        self.parser.add_argument(
            '--{}'.format(ARG_NOPUSH.replace('_', '-')),
            help="Only generate data file without pushing to db.",
            action='store_true'
        )
        self.parser.add_argument(
            '--{}'.format('version'),
            action='version',
            version='minflux {version}'.format(version=__version__)
        )

    @property
    def args(self):
        """Return list of args."""
        return self.parser.parse_args()


def get_arguments():
    """Gets command line arguments."""
    opts = dict()
    parser = Parser()
    for arg in vars(parser.args):
        opts[arg] = getattr(parser.args, arg)
    return opts


def main():
    """Start conversion."""
    args = get_arguments()
    config = yaml.load_yaml(args[ARG_CONFIG])
    util.set_loggers(
        LOGGER,
        file=config[CONF_LOGGER][CONF_FILE],
        level=config[CONF_LOGGER][CONF_LEVEL]
    )
    db_client = dbwrite.InfluxClient(config)
    status = False
    try:
        source = config[CONF_MINT][CONF_FILE]
        LOGGER.debug("Using single file %s", source)
        status = dbwrite.influxdb_write(config, db_client,
                                        source, db_skip=args[ARG_NOPUSH])
    except KeyError:
        source = config[CONF_MINT][CONF_DIR]
        LOGGER.debug("Using source dir %s", source)
        status = True
        for file in glob.glob('{}/*.csv'.format(source)):
            LOGGER.debug("Found %s", file)
            result = dbwrite.influxdb_write(config, db_client,
                                            file, db_skip=args[ARG_NOPUSH])
            if not result:
                LOGGER.error("Could not write %s to database", file)
                status = False
                break

    if status and not args[ARG_NOPUSH]:
        LOGGER.info("Databse write successful! :)")
    elif not status:
        LOGGER.error("Database write unsuccessful :(")
        sys.exit(1)


if __name__ == '__main__':
    main()
