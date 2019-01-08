# Python project for replication failover in a MySQL replication set.
# Classification (U)

# Description:
  This program is used to conduct replication failover in a MySQL replica set, to include switching the best slave to master and selecting a specific slave to become master.


##  This README file is broken down into the following sections:
  * Features
  * Prerequisites
  * Installation
  * Configuration
  * Program Description
  * Program Help Function
  * Help Message
  * Testing
    - Unit
    - Integration
    - Blackbox


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

Create MySQL configuration file.

```
cd config
cp mysql_cfg.py.TEMPLATE mysql_cfg.py
```

Make the appropriate change to the environment.
  * Change these entries in the MySQL setup:
    - passwd = "ROOT_PASSWORD"
    - host = "HOST_IP"
    - name = "HOSTNAME"
    - sid = SERVER_ID

```
vim mysql_cfg.py
chmod 600 mysql_cfg.py
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

Create a MySQL slave configuration file.

```
cp slave.txt.TEMPLATE slave.txt
```

Make the appropriate change to the environment.
  * Change these entries in the MySQL slave setup:
    * NOTE:  Create a new set of entries for each slave in the MySQL replica set.
    - passwd = ROOT_PASSWORD
    - host = HOST_IP
    - name = HOSTNAME
    - sid = SERVER_ID

```
vim slave.txt
chmod 600 slave.txt
```


# Program Descriptions:
### Program: mysql_rep_failover.py
##### Description: Performance monitoring program for a MySQL database.


# Program Help Function:

  The program has a -h (Help option) that will show display an usage message.  The help message will usually consist of a description, usage, arugments to the program, example, notes about the program, and any known bugs not yet fixed.  To run the help command:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
{Python_Project}/mysql-failover/mysql_rep_failover.py -h
```


# Help Message:
  Below is the help message for the program the program.  Run the program with the -h option get the latest help message for the program.

    Program:  mysql_rep_failover.py

    Description:  Administration program for MySQL Replication system.  The
        program has a number of functions to allow the failover of a
        replication system from a master to a slave.  This failover can be done
        to the best slave possible or a designed slave.  The program can also
        be used to show the best slave in a slave replication set and show the
        differences between the slaves in the replication set.  This program is
        assuming that the master is down or otherwise unavailable and will not
        require a master replication configuration file, only a slave
        configuration file.

    WARNING:  This program will allow the changing of the slaves databases to
        new replication configurations, but it does not update the
        slave configuration files or creates new master configuration
        files.  This must be done outside the scope of this program.

    Usage:
        mysql_rep_failover.py -s [path/]file -d path [-F | -G name | -B | -D]
        [-v | -h]

    Arguments:
        -s file => Slave config file.  Will be a text file.  Include the
            file extension with the name.  Can include the path or use
            the -d option path.  Required arg.
        -d dir path => Directory path to the config files. Required arg.
        -F => Select the best slave within the replication set and promote it
            to master and make all other slaves change to the new master.
        -G name => Take the designated name of the slave and promote it
            to master and make all other slaves change to the new master.
            WARNING:  This option could result in loss of transactions
                in the replication set as this option will override the best
                slave promotion and could possibly make a slave which is
                behind the rest of the slaves a master database.
        -B => Displays the name of the current best slave in the
            replication set based on it's current positions compared
            with the other slaves in the set.
        -D => Shows the slaves in the replication set from best to
            worst and displays the differences.
        -v => Display version of this program.
        -h => Help and usage message.

        NOTE 1:  -v or -h overrides the other options.
        NOTE 2:  -F, -G, -B, and -D are XOR arguments.

    Notes:
        Slave(s) configuration file format (filename.txt)
            # Slave 1 configuration {Database Name/Server}
            user = root
            passwd = ROOT_PASSWORD
            host = IP_ADDRESS
            serv_os = Linux or Solaris
            name = HOSTNAME
            port = PORT_NUMBER
            cfg_file DIRECTORY_PATH/my.cnf
            sid = SERVER_ID
            # Slave N configuration {Database Name/Server}
               Repeat rest of above section for Slave 1.

        NOTE:  Include the cfg_file even if running remotely as the file
            will be used in future releases.

    Example:
        mysql_rep_failover.py -s slaves.txt -d config -F



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

```
cd {Python_Project}/mysql-failover
```


### Unit:  help_message
```
test/unit/mysql_rep_failover/help_message.py
```

### Unit:  
```
test/unit/mysql_rep_failover/
```

### Unit:  
```
test/unit/mysql_rep_failover/
```

### Unit:  run_program
```
test/unit/mysql_rep_failover/run_program.py
```

### Unit:  main
```
test/unit/mysql_rep_failover/main.py
```

### All unit testing
```
test/unit/mysql_rep_failover/unit_test_run.sh
```

### Code coverage program
```
test/unit/mysql_rep_failover/code_coverage.sh
```


# Integration Testing:

### Description: Testing consists of integration testing of functions in the mysql_rep_failover.py program.

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

### Configuration:

Create MySQL configuration file.
```
cd test/integration/mysql_rep_failover/config
cp ../../../../config/mysql_cfg.py.TEMPLATE mysql_cfg.py
```

Make the appropriate change to the environment.
  * Change these entries in the MySQL setup.
    - passwd = "ROOT_PASSWORD"
    - host = "HOST_IP"
    - name = "HOSTNAME"
    - sid = SERVER_ID

```
vim mysql_cfg.py
chmod 600 mysql_cfg.py
```

Create a MySQL slave configuration file.

```
cp ../../../../config/slave.txt.TEMPLATE slave.txt
```

Create MySQL definition file.

```
cp ../../../../config/mysql.cfg.TEMPLATE mysql.cfg
```

Make the appropriate change to the MySQL definition setup.
  * Change these entries in the MySQL configuration file:
    - password="ROOT_PASSWORD"
    - socket={BASE_DIR}/mysql/tmp/mysql.sock

```
vim mysql.cfg
chmod 600 mysql.cfg
```

Make the appropriate change to the environment.
  * Change these entries in the MySQL slave setup:
    * NOTE:  Create a new set of entries for each slave in the MySQL replica set.
    - passwd = ROOT_PASSWORD
    - host = HOST_IP
    - name = HOSTNAME
    - sid = SERVER_ID

```
vim slave.txt
chmod 600 slave.txt
```


# Integration test runs for mysql_rep_failover.py:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
cd {Python_Project}/mysql-failover
```


### Integration:  
```
test/integration/mysql_rep_failover/
```

### All integration testing
```
test/integration/mysql_rep_failover/integration_test_run.sh
```

### Code coverage program
```
test/integration/mysql_rep_failover/code_coverage.sh
```


# Blackbox Testing:

### Description: Testing consists of blackbox testing of the mysql_rep_failover.py program.

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

### Configuration:

Create MySQL configuration file.

```
cd test/blackbox/mysql_rep_failover/config
cp ../../../../config/mysql_cfg.py.TEMPLATE mysql_cfg.py
```

Make the appropriate change to the environment.
  * Change these entries in the MySQL setup:
    - passwd = "ROOT_PASSWORD"
    - host = "HOST_IP"
    - name = "HOSTNAME"
    - sid = SERVER_ID

```
vim mysql_cfg.py
chmod 600 mysql_cfg.py
```

Create a MySQL slave configuration file.

```
cp ../../../../config/slave.txt.TEMPLATE slave.txt
```

Create MySQL definition file.

```
cp ../../../../config/mysql.cfg.TEMPLATE mysql.cfg
```

Make the appropriate change to the MySQL definition setup.
  * Change these entries in the MySQL configuration file:
    - password="ROOT_PASSWORD"
    - socket={BASE_DIR}/mysql/tmp/mysql.sock

```
vim mysql.cfg
chmod 600 mysql.cfg
```

Make the appropriate change to the environment.
  * Change these entries in the MySQL slave setup:
    * NOTE:  Create a new set of entries for each slave in the MySQL replica set.
    - passwd = ROOT_PASSWORD
    - host = HOST_IP
    - name = HOSTNAME
    - sid = SERVER_ID

```
vim slave.txt
chmod 600 slave.txt
```


# Blackbox test run for mysql_rep_failover.py:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
cd {Python_Project}/mysql-failover
```


### Blackbox:  
```
test/blackbox/mysql_rep_failover/blackbox_test.sh
```

