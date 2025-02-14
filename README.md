# Python project for replication failover in a MySQL replication set.
# Classification (U)

# Description:
  Used to conduct replication failover in a MySQL replica set, to include switching the best slave to master and selecting a specific slave to become master.


###  This README file is broken down into the following sections:
  * Features
  * Prerequisites
  * Installation
  * Configuration
  * Program Help Function
  * Testing
    - Unit


# Features:
  * Automatically switching the master to the best slave.
  * Selecting a specific slave to become the new master.
  * Displaying the best slave in the replica set.
  * Show all the slaves in the replica set from best to worst.


# Prerequisites:

  * List of Linux packages that need to be installed on the server.
    - python3-pip


# Installation:

Install this project using git.

```
git clone git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/mysql-failover.git
```

Install/upgrade system modules.

NOTE: Install as the user that will run the program.

```
python -m pip install --user -r requirements3.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
```


Install supporting classes and libraries.

```
python -m pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
python -m pip install -r requirements-mysql-lib.txt --target mysql_lib --trusted-host pypi.appdev.proj.coe.ic.gov
python -m pip install -r requirements-mysql-python-lib.txt --target mysql_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
```


# Configuration:

Create a MySQL slave configuration file.  Make the appropriate change to the environment.
  * Change these entries in the MySQL slave setup:
    - user = USER
    - japd = PSWORD
    - rep_user = REP_USER
    - rep_japd = REP_PSWORD
    - host = HOST_IP
    - name = HOST_NAME
    - sid = SERVER_ID
    - port = 3306
    - extra_def_file = 'DIRECTORY_PATH/mysql.cfg'

  * Change these entries only if required:
    - cfg_file = None
    - serv_os = "Linux"
    - port = 3306

  * If SSL connections are being used, configure one or more of these entries:
    - ssl_client_ca = None
    - ssl_client_key = None
    - ssl_client_cert = None

  * Only changes these if necessary and have knowledge in MySQL SSL configuration setup:
    - ssl_client_flag = None
    - ssl_disabled = False
    - ssl_verify_id = False
    - ssl_verify_cert = False

  * TLS version: Set what TLS versions are allowed in the connection set up.
    - tls_versions = []

  * Create a new set of entries for each slave in the MySQL replica set.

```
cp config/slave.txt.TEMPLATE config/slave.txt
vim config/slave.txt
chmod 600 config/slave.txt
```

Create MySQL definition file.  Make the appropriate change to the MySQL definition setup.
  * Change these entries in the MySQL configuration file:
  * Note:  socket use is only required to be set in certain conditions when connecting using localhost.
    - password="PSWORD"
    - socket=DIRECTORY_PATH/mysqld.sock

```
cp config/mysql.cfg.TEMPLATE config/mysql.cfg
vim config/mysql.cfg
chmod 600 config/mysql.cfg
```


# Program Help Function:

  The program has a -h (Help option) that will show display an usage message.  The help message will usually consist of a description, usage, arugments to the program, example, notes about the program, and any known bugs not yet fixed.  To run the help command:

```
mysql_rep_failover.py -h
```


# Testing:

# Unit Testing:

### Installation:

Install the project using the procedures in the Installation section.

# Unit test runs for mysql_rep_failover.py:

### Testing:

```
test/unit/mysql_rep_failover/unit_test_run.sh
test/unit/mysql_rep_failover/code_coverage.sh
```

