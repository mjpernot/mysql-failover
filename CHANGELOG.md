# Changelog
All notable changes to this project will be documented in this file.

The format is based on "Keep a Changelog".  This project adheres to Semantic Versioning.


## [3.0.1] - 2025-05-30
- Updated python-lib to v4.0.1
- Updated mysql-lib to v5.5.1
- Removed support for MySQL 5.6/5.7

### Changed
- Documentation changes.


## [3.0.0] - 2025-02-14
Breaking Changes

- Removed support for Python 2.7.
- Updated mysql-lib v5.4.0
- Updated python-lib v4.0.0

### Changed
- dump_db: Added 'encoding' to open() call.
- Converted strings to f-strings.
- Documentation changes.

### Deprecated
- Support for MySQL 5.6/5.7


## [2.4.5] - 2024-11-18
- Updated python-lib to v3.0.8
- Updated mysql-lib to v5.3.9

### Fixed
- Set chardet==3.0.4 for Python 3.


## [2.4.4] - 2024-11-11
- Updated chardet==4.0.0 for Python 3
- Updated distro==1.9.0 for Python 3
- Updated protobuf==3.19.6 for Python 3
- Updated mysql-connector-python==8.0.28 for Python 3
- Updated mysql-lib to v5.3.8
- Updated python-lib to v3.0.7

### Deprecated
- Support for Python 2.7


## [2.4.3] - 2024-09-27
- Updated simplejson==3.13.2 for Python 3
- Updated python-lib to v3.0.5
- Updated mysql-lib to v5.3.7


## [2.4.2] - 2024-09-04
- Updated mysql-lib to v5.3.6

### Changed
- main: Removed parsing from gen_class.ArgParser call and called arg_parse2 as part of "if" statement.


## [2.4.1] - 2024-02-29
- Updated to work in Red Hat 8
- Updated python-lib to v3.0.3
- Updated mysql-lib to v5.3.4

### Changed
- Set simplejson to 3.12.0 for Python 3.
- Set chardet to 3.0.4 for Python 2.
- Documentation updates.


## [2.4.0] - 2023-08-17
- Upgraded python-lib to v2.10.1
- Replace arg_parser.arg_parse2 with gen_class.ArgParser.

### Changed
- Multiple functions: Replaced the arg_parser code with gen_class.ArgParser code.
- main: Removed gen_libs.get_inst call.


## [2.3.2] - 2022-11-07
- Updated to work in Python 3 too
- Upgraded python-lib to v2.9.4
- Upgraded mysql-lib to v5.3.2

### Changed
- Converted imports to use Python 2.7 or Python 3.


## [2.3.1] - 2022-06-27
- Upgraded python-lib to v2.9.2
- Upgraded mysql-lib to v5.3.1
- Added TLS capability

### Changed
- config/slave.txt.TEMPLATE: Added TLS entry.
- Documentation updates.


## [2.3.0] - 2021-08-20
- Updated to work in MySQL 8.0 and 5.7 environments.
- Updated to work in a SSL environment.
- Updated to use the mysql_libs v5.2.2 library.
- Updated to use gen_libs v2.8.4 library.

### Changed
- promote_designated_slave, promote_best_slave:  Added \*\*kwargs to parameter list and pass to convert_to_master function and add check on master connection status.
- show_best_slave, show_slave_delays:  Added \*\*kwargs to parameter list.
- create_instances, convert_to_master:  Receive slv_key argument and call gen_libs.transpose_dict function.
- main:  Setup slv_key dictionary.
- convert_to_master, create_instances:  Changed cmds_gen.create_cfg_array to gen_libs.create_cfg_array.
- Removed unnecessary \*\*kwargs in function argument list.
- run_program:  Replaced cmds_gen.disconnect with mysql_libs.disconnect and add \*\*kwargs to parameter list and pass to create_instances and called function.
- config/slave.txt.TEMPLATE: Added SSL configuration options.
- config/mysql.cfg.TEMPLATE:  Point to correct socket file.

### Fixed
- promote_designated_slave, promote_best_slave:  Add disconnect for master connection.

### Removed
- cmds_gen module.


## [2.2.0] - 2020-09-11
- Updated to use the mysql_libs v5.0.0 library.
- Validated to work with (much older) mysql.connector v1.1.6 library module.

### Fixed
- config/mysql.cfg.TEMPLATE:  Point to correct socket file.

### Added
- convert_to_master:  Creates MasterRep instance from a SlaveRep instance.

### Changed
- show_slave_delays:  Updated formatting of output.
- show_slave_delays, show_best_slave:  Added return status code.
- promote_designated_slave:  Added call to convert_to_master to convert slave instance to master instance.
- promote_best_slave:  Added call to convert_to_master to convert slave instance to master instance.
- config/slave.txt.TEMPLATE:  Added rep_user and rep_japd entries to configuration file.
- Documentation updates.


## [2.1.1] - 2020-08-07
### Fixed
- main:  Fixed handling command line arguments from SonarQube scan finding.

### Changed
- config/slave.txt.TEMPLATE:  Changed configuration entry name.
- show_best_slave:  Changed variables to a placeholder variables.
- order_slaves_on_gtid:  Changed variable name to standard naming convention.
- promote_best_slave:  Changed variables to a placeholder variables.
- gtid_enabled:  Changed variable name to possible naming conflict.
- run_program:  Changed variable name to standard naming convention.
- Documentation updates.


## [2.1.0] - 2020-01-10
### Fixed
- promote_designated_slave:  Cannot reference class if slave not found in array.
- show_slave_delays:  Fixed problem with mutable default arguments issue.
- show_best_slave:  Fixed problem with mutable default arguments issue.
- promote_designated_slave:  Fixed problem with mutable default arguments issue.
- order_slaves_on_gtid:  Fixed problem with mutable default arguments issue.
- promote_best_slave:  Fixed problem with mutable default arguments issue.
- gtid_enabled:  Fixed problem with mutable default arguments issue.
- create_instances:  Fixed problem with mutable default arguments issue.
- run_program:  Fixed problem with mutable default arguments issue.

### Changed
- config/slave.txt.TEMPLATE:  Added extra_def_file entry to file.
- run_program:  Replaced sys.exit() calls with print calls.
- main:  Added program lock functionality to program.
- main:  Added new option -y to the program.
- main:  Refactored if statements.
- show_slave_delays:  Changed variable name to standard convention.
- show_best_slave:  Changed variable name to standard convention.
- promote_designated_slave:  Changed variable name to standard convention.
- order_slaves_on_gtid:  Changed variable name to standard convention.
- promote_best_slave:  Changed variable name to standard convention.
- create_instances:  Changed variable name to standard convention.
- gtid_enabled:  Changed variable name to standard convention.
- run_program:  Changed variable name to standard convention.
- Documentation update.


## [2.0.1] - 2018-11-30
### Fixed
- run_program:  Added disconnect call for slaves in case of error status returned.

### Changed
- show_best_slave:  Changed "\_" to "\_\_" for function argument return.
- promote_best_slave:  Changed "\_" to "\_\_" for function argument return.


## [2.0.0] - 2018-05-21
Breaking Change

### Changed
- Changed "mysql_libs" calls to new naming schema.
- Changed "cmds_gen" calls to new naming schema.
- Changed "gen_libs" calls to new naming schema.
- Changed "arg_parser" calls to new naming schema.
- Changed function names from uppercase to lowercase.
- Setup single-source version control.


## [1.2.0] - 2018-04-27
### Changed
- Changed "commands" to "mysql_libs" module reference.

### Added
- Added single-source version control.


## [1.1.0] - 2017-08-21
### Changed
- Help_Message:  Replace docstring with printing the programs \_\_doc\_\_.
- Change single quotes to double quotes.
- Convert program to use local libraries from ./lib directory.


## [1.0.0] - 2017-01-10
- Initial creation.

