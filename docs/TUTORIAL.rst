Minflux Tutorial
================

This tutorial assumes you have already installed InfluxDB.  It also assumes your InfluxDB instance is running on ``localhost:8086``.  If it is not, please adjust these instructions accordingly. 

The following topics will be covered:

- Creating a user and database for Minflux within InfluxDB
- Installing Minflux
- Setting up your ``config.yaml`` file for Minflux
- Performing database queries
- Data visualization recommendations

Set up InfluxDB
===============

Create Database
---------------

In a command prompt, use the ``influx`` command to get started.  

First, we need to create the database we'll be using to push the data generated with ``minflux``.  We'll call this database ``minflux_db``, but feel free to use any name you like.

.. code::
    
    > CREATE DATABASE "minflux_db"


This command creates the database and assigns the ``autogen`` .. _Retention Policy: https://docs.influxdata.com/influxdb/v1.3/query_language/database_management/#retention-policy-management which will retain the data infinitely.  If you'd rather only store your data for a finite amount of time, you can create a custom retention policy instead.  Here, we will create a retention policy called ``five_years`` for a duration of, well, five years.  InfluxDB does not allow the use of years as the duration, so we'll have to use either days or weeks.  We can do this with the following command.

.. code::
    
   > CREATE RETENTION POLICY "five_years" ON "minflux_db" DURATION 260w REPLICATION 1 DEFAULT


Verify that your retention policy was created via the following command sequence (the result should look similar to what is shown below).

.. code::
    
    > USE minflux_db
    > SHOW RETENTION POLICIES
    name        duration    sharedGroupDuration replicaN default
    ----        --------    ------------------- -------- -------
    autogen     0s          168h0m0s            1        false
    five_years  43680h0m0s  168h0m0s            1        true

    
Create a User
-------------

Now we're going to create a dedicated, non-admin, user for the minflux database.  We will create a user ``minflux`` with a password of ``password123`` (please don't use that as your password, this is just an example!).

.. code::
    
   > CREATE USER minflux WITH PASSWORD 'password123'


The next step is to grant the ``minflux`` user all privileges on the ``minflux_db`` database.  This is done with the following command.

.. code::
    
   > GRANT ALL ON "minflux_db" TO "minflux"


You can verify these privileges via the ``SHOW GRANTS FOR "minflux"`` command, which should output something like the following:

.. code::
    
   > SHOW GRANTS FOR "minflux"
    database    privilege
    --------    ---------
    minflux_db  ALL PRIVILEGES


Install Minflux
================

Currently, installtion of Minflux requires cloning the master branch of the GitHub repository and building the module yourself.  To do so, navigate to where you want to install Minflux and perform the following commands:

.. code:: bash

    $ git clone https://github.com/fronzbot/minflux.git
    $ cd minflux
    $ sudo python3 setup.py install

This will install all neccessary dependencies and should finish without errors.
    
Create ``config.yaml``
----------------------

You can now create your ``config.yaml`` file which will tell ``minflux`` how to interact with your InfluxDB installation.  Where you place your ``config.yaml`` is totally up to you, but we're going to assume you're placing it in ``/home/username/minflux``.  The first step is to create the file with ``touch /home/username/minflux/config.yaml``.  Then, open that file with your favorite text editor and add the following contents:

.. code:: yaml

    influxdb:
        host: 'http://localhost'
        port: 8086
        user: 'minflux'
        password: 'password123'
        dbname: 'minflux_db'

Add Mint to ``config.yaml``
---------------------------

Currently, transactions from mint must be manually saved from their webclient into a csv format.  Mint has a handy "Export to CSV" function which you can use for this purpose.  For this tutorial, it is assumed that you are saving your csv files in ``/home/user/mint``.  This directory will need to be passed to ``minflux`` via an entry in ``config.yaml``.  We will also add an archiving feature so that once ``minflux`` processes your csv, it will be compressed and moved to an ``archive`` directory.  In this case, that directory will be in ``/home/user/mint/archive``.

.. code:: yaml

    influxdb:
        host: 'http://localhost'
        port: 8086
        user: 'minflux'
        password: 'password123'
        dbname: 'minflux_db'
    mint:
        directory: '/home/user/mint'
        archive:

By telling ``minflux`` that you're using a directory, it will grab *all* csv files in that directory and process them.  This makes it very convenient if you have large amounts of data segmented across multiple files.


Run Minflux
============

You can now run ``minflux`` so that it parses the csv file and writes it to your InfluxDB database.  To do so, you must explicitly tell it where your config file is located via the ``--config`` flag, like so:

.. code:: bash

    $ minflux --config /home/user/mint

When this is done, you should see the following in your log:

.. code:: bash

    $ ... INFO Databse write successful! :)

Example InfluxDB Query
=======================

Now that we've push our data to InfluxDB, we can perform some queries to see things like money spent per category or per vendor.  Say you have a category in Mint called ``Shopping`` and you want to see how much you spent over a certain time range.  First, double check that your measurement exists by running the ``SHOW MEASUREMENTS`` command within InfluxDB:

.. code:: bash

    > SHOW MEASUREMENTS
    name
    ----
    Best Buy
    Amazon
    Shopping
    Restaurants
    Income
    Checking
    Chef's Restaurants

We see that our categort shopping is indeed listed, so we can use it in a query to get our data.  Now, let's look at all of the data we have in our ``Shopping`` measurement:

.. code:: bash

    > SELECT * FROM Shopping
    name: Shopping
    time                account     category value  vendor
    ----                -------     -------- -----  ------ 
    1483833600000000000 Checking    Shopping -10.50 Best Buy
    1484006400000000000 Checking    Shopping -27.87 Amazon
    1484265600000000000 Checking    Shopping -34.14 Best Buy
    1484784000000000000 Checking    Shopping  10.50 Best Buy
    1485043200000000000 Checking    Shopping -8.75  Amazon
    1485648000000000000 Checking    Shopping -47.02 Amazon
    1485648000000000000 Checking    Shopping -33.65 Amazon

So here we see a few transactions, some where we bought stuff from Amazon, other from Best Buy.  We even see that we have a credit from Best Buy (looks like we returned the first item in the list).  The dates are... hard to understand.  They're listed in epoch nano-seconds (how many one one-billionth seconds since January 1, 1970).  We chan change this to something more human-friendly via ``PRECISION RFC3339``.  Now, if we re-do our query, we'll see:

.. code:: bash

    > SELECT * FROM Shopping
    name: Shopping
    time                 account     category value  vendor
    ----                 -------     -------- -----  ------ 
    2017-01-08T00:00:00Z Checking    Shopping -10.50 Best Buy
    2017-01-10T00:00:00Z Checking    Shopping -27.87 Amazon
    2017-01-13T00:00:00Z Checking    Shopping -34.14 Best Buy
    2017-01-19T00:00:00Z Checking    Shopping  10.50 Best Buy
    2017-01-22T00:00:00Z Checking    Shopping -8.75  Amazon
    2017-01-29T00:00:00Z Checking    Shopping -47.02 Amazon
    2017-01-29T00:00:00Z Checking    Shopping -33.65 Amazon

Cool!  So, now what can we do?  Well, let's look at how much money we spent in the shopping category from January 1st to January 15th.

.. code:: bash

    > SELECT SUM("value") FROM Shopping WHERE time >= '2017-01-01T00:00:00Z' AND time <= '2017-01-15T00:00:00Z'
    time                 sum
    ----                 ---
    2017-01-01T00:00:00Z -72.51

We can also do cool things like group by vendor, so we can see how much spent in a month in a catgeory per vendor.

.. code:: bash

    > SELECT SUM("value") FROM Shopping WHERE time >= '2017-01-01T00:00:00Z' AND time <= '2017-01-31T00:00:00Z' GROUP BY "vendor"
    name: Shopping
    tags: vendor=Amazon
    time
    ----
    2017-01-01T00:00:00Z -117.29

    name: Shopping
    tags: vendor=Best Buy
    time
    ----
    2017-01-01T00:00:00Z -34.14

There's a whole lot more you can do, but this should have been a decent overview of the basics.

Data Visualization
===================

Being able to query data is useful, for sure, but visualizing it is just as important.  We won't cover set up here, but we highly recommend using .. _Grafana: http://docs.grafana.org/ to visualize data.  It has a built-in GUI for InfluxDB queries which makes displaying graphs incredibly easy.

