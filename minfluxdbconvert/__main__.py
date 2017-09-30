"""Primary module for minfluxdb-convert."""
import sys
import glob
import logging
import minfluxdbconvert.util as util
import minfluxdbconvert.yaml as yaml
import minfluxdbconvert.dbwrite as dbwrite
from minfluxdbconvert.const import (CONF_FILE, CONF_MINT, CONF_LOGGER,
                                    CONF_LEVEL, CONF_DIR)
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
