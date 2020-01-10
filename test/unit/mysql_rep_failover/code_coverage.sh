#!/bin/bash
# Unit test code coverage for program module.
# This will run the Python code coverage module against all unit test modules.
# This will show the amount of code that was tested and which lines of code
#   that was skipped during the test.

coverage erase

echo ""
echo "Running unit test modules in conjunction with coverage"
coverage run -a --source=mysql_rep_failover test/unit/mysql_rep_failover/help_message.py
coverage run -a --source=mysql_rep_failover test/unit/mysql_rep_failover/show_slave_delays.py

echo ""
echo "Producing code coverage report"
coverage combine
coverage report -m
