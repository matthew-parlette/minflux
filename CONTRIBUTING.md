# Contributing to minfluxdb-convert

The following outlines what this project is about and how to contribute.

## What this project is about
minfluxdb-convert is intended as a personal finance tool in that it takes raw data exported from an aggregation service, specifically [Mint](https://mint.com), and converts it to an [InfluxDB](https://www.influxdata.com/)-friendly format.  This allows for long-term data storage in a format that's conducive for plotting long-term trends and correlations.  The intention of this project is to supplement or replace custom spreadsheet usage and, instead, allow for all of your financial data to be accessed via a database (such as on a home server).

## Prerequisites
Currently, this package is intended for use on Linux.  Windows is not currently supported.  In addition, this project only works with Python 3.4+ and Python 2.7 support is not planned.

## Setting up local development area
All development is done on the `master` branch of the minfluxdb-convert project.  To get started with a development area, first you need to fork the repo from GitHub.  Once you do this, you can clone your forked copy of the repo into your work area with the following:

```bash
$ git clone https://github.com/YOUR_GIT_USERNAME/minfluxdb-convert.git
$ cd minfluxdb-convert
$ git remote add upstream https://github.com/fronzbot/minfluxdb-convert.git
```

## Running the module locally
For rapid test development, you can use the following command to run the minfluxdb-convert package.

```bash
$ python3 -m minfluxdbconvert --config=/path/to/config.yaml [OPTIONS]
```

```yaml
influxdb:
 host: http://localhost
 port: 8086
 user: root
 password: root
 dbname: test
mint:
 file: /home/user/mint.csv
```

If you do not have an InfluxDB instance you can push results to, you can simply use the `--skip-push` flag as an option when you run `minfluxdbconvert`.  This will run the whole script except for the write to an InfluxDB instance.  The data is instead dumped as a json file which can be used for debugging/verification.

### An alternative is to install the package as if you were an end user.  This step would be required after every change, so it's more cumbersome than the previous method (but has the benefit of ensuring there are no dependency issues with your code).

```bash
$ sudo python3 setup.py install
$ mfdb --config=/path/to/config.yaml [OPTIONS]
```

## Style Guidelines
minfluxdb-convert enforces [PEP8 style](https://www.python.org/dev/peps/pep-0008/) on all submitted code.  Code is automatically test as part of your pull request via [Travis CI](https://travis-ci.org/fronzbot/minfluxdb-convert).  A quick summary of the most common style violations:

- Line length limited to 79 characters.
- Use four spaces per indentation level.  Tabs not allowed.
- Comments should be full sentences and end with a period.
- No trailing whitespace.
- No whitespace on empty lines.

### Other recommendations
Some styles are not enforced by PEP, but are required for your pull request to be accepted.  These extra style guidelines help to increase readability, so please make a conscious effort to follow them.

#### QUOTES
Use single quotes `'` for single word and double quotes `"` for multi-word sentences.

```python
CONF_USERNAME = 'username'
ATTR_DESCRIPTION = "This project is awesome."
json_body = {
 'data'= ['foo', 'bar']
}
```

#### LOG MESSAGES
Logging formats are handled automatically, so adding extra log messages only need to be done as follows:

```python
LOGGER.error("Oh crap, found an error in value %s", value)
```

## Testing your code
Local tests are done via `tox` which can be installed with the following command:

```bash
$ pip3 install tox
```

You can then test the code via:

```bash
$ tox
```

It is *highly* recommended to run `tox` before submitting your PR to avoid annoying fixes.

### Running single tests
In order to speed up development you can run specific tests (full test suite, only linting, etc.).  This is done via the `-e` flag and selecting an environment.  For example, `tox -e py35` runs unit tests in Python 3.5 and `tox -e lint` runs the linters only.

If you are adding a new requirement in your code (and added it to the `requirements.txt` or `requirements_test.txt` file), you will need to regenerate the requirements for tox via the `-r` flag.  For example `tox -r` will run the full test suite and force regeneration of requirements.

You can run single tests if you're only modifying a single file using the following example syntax:

```bash
# Run test_main tests and stop after first failure
$ tox -e py35 -- tests/test_main.py -x
# Run test with specified name
$ tox -e py35 -- tests/test_main.py -k test_no_arguments
```

### Notes on PyLint and PEP8
If you simply cannot avoid a PyLint warning, you can add a comment to your code that will disable the warning like so: `# pylint: disable=YOUR-ERROR-NAME`

## Submitting your work
Each feature being added should be in its own pull request (ie. its own branch).  Please avoid adding multiple features to a single PR as it become very difficult to review.  To submit your improvement/fix/feature, use the following steps:

1. From your fork's master branch, create a new branch to hold your changes: `git checkout -b some-feature`.
2. Make your changes.
3. If adding new functionality, consider if you will need to add unit tests to verify functionality.
4. Test your changes locally with `tox` as described above.
5. Once everything looks good, commit your changes: `git add.` `git commit -m "Added some feature"`.
6. Push your committed changed to your GitHub fork: `git push origin HEAD`.
7. Follow [these steps](https://help.github.com/articles/creating-a-pull-request/) to submit your pull request.
8. Keep an eye on your PR for comments/suggestions as well as any style violations automatically detected by [Hound](https://houndci.com/)


## Catching up with reality
If it's taking a while to implement your feature, you can catch up with the `master` branch by using `git rebase`.  This will pull the latest changes in locally, rewind your commits, bring the latest changes from minfluxdb-convert, and replay all of your commits on top.

```bash
# Run this from your local feature branch
$ git fetch upstream master
$ git rebase upstream/master
```

If there are any conflicts detected during rebase, repeat the following process until resolved:

1. `git status` shows the file containing the conflict.  Edit the file and resolve the lines between `<<<< | >>>>`.
2. Add the modified file via either `git add <file>` or `git add.`.
3. Continue with rebase: `git rebase --continue`.
4. Repeat until all conflicts are resolved.

After rebasing, if you try to push to your GitHub fork, you'll receive an error stating that your history has diverged from the original branch.  In order to get your fork up-to-date with your local branh, you need to force push:

```bash
# Run this from your local feature branch
$ git push origin --force
```