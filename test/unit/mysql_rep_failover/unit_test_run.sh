#!/bin/bash
# Unit testing program for the program module.
# This will run all the units tests for this program.
# Will need to run this from the base directory where the module file
#   is located at.

echo ""
echo "Unit testing..."
test/unit/mysql_rep_failover/convert_to_master.py
test/unit/mysql_rep_failover/create_instances.py
test/unit/mysql_rep_failover/gtid_enabled.py
test/unit/mysql_rep_failover/help_message.py
test/unit/mysql_rep_failover/main.py
test/unit/mysql_rep_failover/order_slaves_on_gtid.py
test/unit/mysql_rep_failover/promote_best_slave.py
test/unit/mysql_rep_failover/promote_designated_slave.py
test/unit/mysql_rep_failover/run_program.py
test/unit/mysql_rep_failover/show_best_slave.py
test/unit/mysql_rep_failover/show_slave_delays.py
