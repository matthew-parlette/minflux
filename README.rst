minfluxdb-convert
===================
A python tool to take a transaction log from https://mint.co and convert it for import into an influxdb database

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

Create a configuration file called ``db.yaml`` with the following contents:

.. code:: yaml

	influxdb:
		host: <your_host>
		port: <port number>
		user: <db username>
		password: <db password>
		dbname: <name of db>
	mintcsv:
		file: <location of csv file>

Run converter tool:
``mfdb <opts>``

Available options:
``--skip-push`` just generates json file and does not push to database (useful for debug)
