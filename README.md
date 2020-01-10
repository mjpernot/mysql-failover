# Python project for replication failover in a MySQL replication set.
# Classification (U)

# Description:
  This program is used to conduct replication failover in a MySQL replica set, to include switching the best slave to master and selecting a specific slave to become master.


##  This README file is broken down into the following sections:
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
    - python-libs
    - python-devel
    - git
    - python-pip

  * Local class/library dependencies within the program structure.
    - lib/cmds_gen
    - lib/arg_parser
    - lib/gen_libs
    - lib/gen_class
    - mysql_lib/mysql_libs


# Installation:

Install this project using git.
  * Replace **{Python_Project}** with the baseline path of the python program.

```
umask 022
cd {Python_Project}
git clone git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/mysql-failover.git
```

Install/upgrade system modules.

```
cd mysql-failover
sudo bash
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.

```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-mysql-lib.txt --target mysql_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target mysql_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
```

# Configuration:

Create a MySQL slave configuration file.

```
cp slave.txt.TEMPLATE slave.txt
```

Make the appropriate change to the environment.
  * Change these entries in the MySQL slave setup:
    - passwd = ROOT_PASSWORD
    - host = HOST_IP
    - name = HOSTNAME
    - sid = SERVER_ID
    - extra_def_file = {Python_Project}/config/mysql.cfg
  * Create a new set of entries for each slave in the MySQL replica set.

```
vim slave.txt
chmod 600 slave.txt
```

Create MySQL definition file.

```
cp mysql.cfg.TEMPLATE mysql.cfg
```

Make the appropriate change to the MySQL definition setup.
  * Change these entries in the MySQL configuration file:
    - password="ROOT_PASSWORD"
    - socket={BASE_DIR}/mysql/tmp/mysql.sock

```
vim mysql.cfg
chmod 600 mysql.cfg
```


# Program Help Function:

  The program has a -h (Help option) that will show display an usage message.  The help message will usually consist of a description, usage, arugments to the program, example, notes about the program, and any known bugs not yet fixed.  To run the help command:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
{Python_Project}/mysql-failover/mysql_rep_failover.py -h
```


# Testing:


# Unit Testing:

### Description: Testing consists of unit testing for the functions in the mysql_rep_failover.py program.

### Installation:

Install this project using git.
  * Replace **{Python_Project}** with the baseline path of the python program.
  * Replace **{Branch_Name}** with the name of the Git branch being tested.  See Git Merge Request.

```
umask 022
cd {Python_Project}
git clone --branch {Branch_Name} git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/mysql-failover.git
```

Install/upgrade system modules.

```
cd mysql-failover
sudo bash
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.

```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-mysql-lib.txt --target mysql_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target mysql_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
```


# Unit test runs for mysql_rep_failover.py:
  * Replace **{Python_Project}** with the baseline path of the python program.

### Unit testing:
```
cd {Python_Project}/mysql-failover
test/unit/mysql_rep_failover/help_message.py
test/unit/mysql_rep_failover/main.py
test/unit/mysql_rep_failover/run_program.py
test/unit/mysql_rep_failover/show_slave_delays.py
```

### All unit testing
```
test/unit/mysql_rep_failover/unit_test_run.sh
```

### Code coverage program
```
test/unit/mysql_rep_failover/code_coverage.sh
```

