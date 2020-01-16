# Changelog
All notable changes to this project will be documented in this file.

The format is based on "Keep a Changelog".  This project adheres to Semantic Versioning.


## [2.1.0] - 2020-01-10
### Changed
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

