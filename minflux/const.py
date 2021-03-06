"""Various constants used within minflux."""

MAJOR_VERSION = 0
MINOR_VERSION = 0
PATCH_VERSION = 11

__version__ = '{}.{}.{}'.format(MAJOR_VERSION, MINOR_VERSION, PATCH_VERSION)

PROJECT_NAME = 'minflux'
PROJECT_LICENSE = 'MIT'
PROJECT_AUTHOR = "Kevin Fronczak"
PROJECT_COPYRIGHT = " 2017, {}".format(PROJECT_AUTHOR)
PROJECT_URL = 'https://github.com/fronzbot/minflux'
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
CONF_NETSUM = 'net_sum'
CONF_EXCLUDE = 'exclude'
CONF_VENDOR = 'vendor'
CONF_CATEGORY = 'category'
CONF_ACCOUNT = 'account'
CONF_DIR = 'directory'
CONF_ARCHIVE = 'archive'
CONF_SUM = 'sum'

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
