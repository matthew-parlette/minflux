minfluxdb-convert |Build| |Coverage| |Versions|
================================================
A python tool to take a transaction log from https://mint.com and convert it for import into an influxdb database

Disclaimer
==========
This module is currently under development and has not been thoroughly tested.  Use at your own risk (or wait until script is more stable)

Usage
=======
Clone repo:

.. code::bash

    $ git clone https://github.com/fronzbot/minfluxdb-convert.git

Install:

.. code::bash
    
    $ cd minfluxdb-convert
    $ sudo python3 setup.py install
    
Create a configuration file called ``config.yaml`` with the following contents:

.. code:: yaml

	influxdb:
		host: <your_host>
		port: <port number>
		user: <db username>
		password: <db password>
		dbname: <name of db>
	mint:
		file: <location of csv file>
        directory: <directory of multiple csv files USE THIS OR FILE, NOT BOTH>

Optionally, the logger can be customized by adding the following to your ``config.yaml``:

.. code:: yaml
    
    logger:
        file: <log file location> (optional)
        level: <debug|info|warning|error|critical> (optional, default is info)

Run converter tool:
``mfdb --config=/loc/of/config/file [opts]``

Available options:
``--skip-push`` just generates json file and does not push to database (useful for debug)

Features
=========
InfluxDB does not allow for cross measurement, preventing a summation of data.  For example, if you have 'Income', 'Bonus', 'ESPP' as categories, you cannot sum them by default.  Now, to get around this (kind of) three measurements are added for the same data:
- One for category
- One for account
- One for vendor

This allows for more customization (at the expense of a larger database).

Another feature is the ability to retrieve a net sum across all measurements.  Here, there may be some categories or account you want to exclude from the calulation, so this is handled by adding the following to your ``config.yaml``:

.. code:: yaml

    net_sum:
        exclude:
            account:
                - account name to exclude
                - account name to exclude #2
            vendor:
                - vendor to exclude
            category:
                - category to exclude
                - category to exclude

If anything changes with what you need to exclude, you can always go in and re-generate the data (timestamps don't change so everything should be overwritten properly).  A future improvement would be to add a 'regenerate-all' flag that, given a directory, will regenerate all of the influxdb data for each csv in that directory.

Additionally, the following line can be added to allow for archiving of processed csv files:

.. code::yaml

    mint:
        ...
        archive:
            directory: <optional archive directory>
        ...

Once ``minfluxdb-convert`` writes your csv files to the database, the file will be compressed and moved the specified archive directory (defaults to a directory named ``archive`` in the directory where your csv files are, if not specified).
        
.. |Build| image:: https://travis-ci.org/fronzbot/minfluxdb-convert.svg?branch=master
   :target: https://travis-ci.org/fronzbot/minfluxdb-convert
.. |Coverage| image:: https://coveralls.io/repos/github/fronzbot/minfluxdb-convert/badge.svg?branch=master
   :target: https://coveralls.io/github/fronzbot/minfluxdb-convert?branch=master
.. |Versions| image:: https://img.shields.io/badge/python-3.4%2C3.5%2C3.6-blue.svg
