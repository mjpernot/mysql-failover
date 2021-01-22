#!/bin/bash
# Unit test code coverage for SonarQube to cover all modules.
# This will run the Python code coverage module against all unit test modules.
# This will show the amount of code that was tested and which lines of code
#       that was skipped during the test.

coverage erase

echo ""
echo "Running unit test modules in conjunction with coverage"
coverage run -a --source=mysql_rep_failover test/unit/mysql_rep_failover/convert_to_master.py
coverage run -a --source=mysql_rep_failover test/unit/mysql_rep_failover/create_instances.py
coverage run -a --source=mysql_rep_failover test/unit/mysql_rep_failover/gtid_enabled.py
coverage run -a --source=mysql_rep_failover test/unit/mysql_rep_failover/help_message.py
coverage run -a --source=mysql_rep_failover test/unit/mysql_rep_failover/main.py
coverage run -a --source=mysql_rep_failover test/unit/mysql_rep_failover/order_slaves_on_gtid.py
coverage run -a --source=mysql_rep_failover test/unit/mysql_rep_failover/promote_best_slave.py
coverage run -a --source=mysql_rep_failover test/unit/mysql_rep_failover/promote_designated_slave.py
coverage run -a --source=mysql_rep_failover test/unit/mysql_rep_failover/run_program.py
coverage run -a --source=mysql_rep_failover test/unit/mysql_rep_failover/show_best_slave.py
coverage run -a --source=mysql_rep_failover test/unit/mysql_rep_failover/show_slave_delays.py

echo ""
echo "Producing code coverage report"
coverage combine
coverage report -m
coverage xml -i
