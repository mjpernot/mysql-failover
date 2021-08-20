# Changelog
All notable changes to this project will be documented in this file.

The format is based on "Keep a Changelog".  This project adheres to Semantic Versioning.


## [2.3.0] - 2021-08-20
- Updated to work in MySQL 8.0 and 5.7 environments.
- Updated to work in a SSL environment.
- Updated to use the mysql_libs v5.2.2 library.

### Changed
- config/slave.txt.TEMPLATE: Added SSL configuration options.
- config/mysql.cfg.TEMPLATE:  Point to correct socket file.


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

