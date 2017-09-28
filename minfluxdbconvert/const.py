MAJOR_VERSION = 0
MINOR_VERSION = 0
PATCH_VERSION = '1.dev0'

__version__ = '{}.{}.{}'.format(MAJOR_VERSION, MINOR_VERSION, PATCH_VERSION)

PROJECT_NAME = 'minfluxdb-convert'
PROJECT_LICENSE = 'MIT'
PROJECT_AUTHOR = 'Kevin Fronczak'
PROJECT_COPYRIGHT = ' 2017, {}'.format(PROJECT_AUTHOR)
PROJECT_URL = 'https://github.com/fronzbot/minfluxdb-convert'
PROJECT_EMAIL = 'kfronczak@gmail.com'

#### CONFIG ####
CONF_INFLUX = 'influxdb'
CONF_MINT = 'mint'
CONF_USER = 'user'
CONF_PASSWORD = 'password'
CONF_DBNAME = 'dbname'
CONF_HOST = 'host'
CONF_PORT = 'port'
CONF_FILE = 'file'
CONF_LOGGER = 'logger'
CONF_LEVEL = 'level'

#### ATTRIBUTES ####
ATTR_DATE = 'date'
ATTR_DESC = 'description'
ATTR_LABELS = 'labels'
ATTR_NOTES = 'notes'
ATTR_ACCOUNT = 'account_name'
ATTR_CATEGORY = 'category'
ATTR_TYPE = 'transaction_type'
ATTR_AMOUNT = 'amount'

#### ARGUMENTS ####
ARG_CONFIG = 'config'
ARG_NOPUSH = 'skip_push'