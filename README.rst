minfluxdb-convert
===================
A python tool to take a transaction log from https://mint.com and convert it for import into an influxdb database

Disclaimer
==========
This module is currently under development and has not been thoroughly tested.  Use at your own risk (or wait until script is more stable)

Usage
=======
Clone repo:
``git clone https://github.com/fronzbot/minfluxdb-convert.git``

Install:
``cd minfluxdb-convert``
``python3 setup.py install``

Create a configuration file called ``config.yaml`` with the following contents:

.. code:: yaml

	influxdb:
		host: <your_host>
		port: <port number>
		user: <db username>
		password: <db password>
		dbname: <name of db>
	mintcsv:
		file: <location of csv file>

Optionally, the logger can be customized by adding the following to your ``config.yaml``:

.. code:: yaml
    
    logger:
        file: <log file location> (optional)
        level: <debug|info|warning|error|critical> (optional, default is info)

Run converter tool:
``mfdb --config=/loc/of/config/file [opts]``

Available options:
``--skip-push`` just generates json file and does not push to database (useful for debug)
