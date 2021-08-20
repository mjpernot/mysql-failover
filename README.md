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
    - git
    - python-pip

  * Local class/library dependencies within the program structure.
    - python-lib
    - mysql-lib


# Installation:

Install this project using git.
  * From here on out, any reference to **{Python_Project}** or **PYTHON_PROJECT** replace with the baseline path of the python program.

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

  * Create a new set of entries for each slave in the MySQL replica set.

```
cp slave.txt.TEMPLATE slave.txt
vim slave.txt
chmod 600 slave.txt
```

Create MySQL definition file.  Make the appropriate change to the MySQL definition setup.
  * Change these entries in the MySQL configuration file:
    - password="PASSWORD"
    - socket=DIRECTORY_PATH/mysql.sock

```
cp mysql.cfg.TEMPLATE mysql.cfg
vim mysql.cfg
chmod 600 mysql.cfg
```


# Program Help Function:

  The program has a -h (Help option) that will show display an usage message.  The help message will usually consist of a description, usage, arugments to the program, example, notes about the program, and any known bugs not yet fixed.  To run the help command:

```
{Python_Project}/mysql-failover/mysql_rep_failover.py -h
```


# Testing:

# Unit Testing:

### Installation:

Install the project using the procedures in the Installation section.

# Unit test runs for mysql_rep_failover.py:

### Testing:

```
cd {Python_Project}/mysql-failover
test/unit/mysql_rep_failover/unit_test_run.sh
```

### Code coverage:

```
cd {Python_Project}/mysql-failover
test/unit/mysql_rep_failover/code_coverage.sh
```

