"""Primary module for minfluxdb-convert."""
import sys
import json
import os
import logging
from influxdb import InfluxDBClient
import minfluxdbconvert.util as util
import minfluxdbconvert.reader as reader

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
LOGGER.addHandler(ch)


def create_json_file(config, csvfile):
    """Converts csv from mint into json file."""
    Mint = reader.TransactionReader(csvfile)
    json_body = list()
    for entry in Mint.data:
        value = util.convert_value(entry[Mint.headers['Amount']],
                                   entry[Mint.headers['Transaction Type']]
                                   )
        json_entry = {'measurement': entry[Mint.headers['Category']],
                      'tags': {
                          'vendor': entry[Mint.headers['Description']],
                          'label': entry[Mint.headers['Labels']],
                          'notes': entry[Mint.headers['Notes']],
                          'account': entry[Mint.headers['Account Name']],
                          },
                      'time': util.date_to_epoch(entry[Mint.headers['Date']]),
                      'fields': {
                          'value': value
                          }
                      }
        json_body.append(json_entry)
    return json_body

# TODO: Currently a terrible implementation and not working...
def validate_config(config):
    """Ensures yaml config file loaded properly."""
    if ['influxdb', 'mintcsv'] is not config.keys():
        LOGGER.error('Invalid config: Missing keys (requires both influxdb and mintcsv keys)')
        sys.exit(1)
    if ['host', 'port', 'dbname', 'user', 'password'] is not config['influxdb'].keys():
        LOGGER.error('Invalid config: influxdb -> Missing required keys')
        sys.exit(1)

    # Check that mint file given is actually readable
    if not os.path.isfile(config['mintcsv']['file']):
        LOGGER.error('Invalid config: Given mintcsv transaction file cannot be found.')
        sys.exit(1)

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
    config = util.load_yaml(args['db_cfg'])
    #validate_config(config)

    source_file = config['mintcsv']['file']

    json_body = create_json_file(config, source_file)

    if args['skip_push']:
        LOGGER.warn('Skipping database write.')
        json_info = json.dumps(json_body)
        with open('dump.json', 'w') as outfile:
            json.dump(json_info, outfile)
        LOGGER.info('Data sent to {}/dump.json'.format(os.getcwd()))
        sys.exit()
    else:
        host = config['influxdb']['host']
        port = config['influxdb']['port']
        db = config['influxdb']['dbname']
        user = config['influxdb']['user']
        password = config['influxdb']['password']

        client = InfluxDBClient(host, port, user, password, dbname)
        client.write_points(json_body)

    LOGGER.warn('Databse write successful! :)')
    sys.exit()


if __name__ == "__main__":
    main()
