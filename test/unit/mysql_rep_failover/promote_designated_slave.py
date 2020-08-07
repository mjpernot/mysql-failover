#!/usr/bin/python
# Classification (U)

"""Program:  promote_designated_slave.py

    Description:  Unit testing of promote_designated_slave in
        mysql_rep_failover.py.

    Usage:
        test/unit/mysql_rep_failover/promote_designated_slave.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

# Third-party
import mock

# Local
sys.path.append(os.getcwd())
import mysql_rep_failover
import lib.gen_libs as gen_libs
import version

__version__ = version.__version__


class SlaveRep(object):

    """Class:  SlaveRep

    Description:  Class stub holder for mysql_class.SlaveRep class.

    Methods:
        __init__ -> Class initialization.
        remove -> Stub holder for mysql_class.SlaveRep.remove method.

    """

    def __init__(self, name, exe_gtidset, gtid_mode):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:
            (input) name -> Name of slave.
            (input) exe_gtidset -> GTID position.
            (input) gtid_mode -> True|False - GTID is turned on.

        """

        self.name = name
        self.exe_gtidset = exe_gtidset
        self.gtid_mode = gtid_mode
        self.master = None
        self.slave = None

    def remove(self, master):

        """Method:  remove

        Description:  Stub holder for mysql_class.SlaveRep.remove method.

        Arguments:
            (input) master -> Master name.

        """

        self.master = master

        return True

    def append(self, slave):

        """Method:  append

        Description:  Stub holder for mysql_class.SlaveRep.append method.

        Arguments:
            (input) slave -> Slave name.

        """

        self.slave = slave

        return True


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_one_failed_switch -> Test switch to new master failed for 1 slave.
        test_failed_all_switch -> Test switch to new master failed for all.
        test_slv_not_found -> Test with no master found in slave list.
        test_no_slave -> Test with only no slaves in list.
        test_one_slave -> Test with only one slave in list.
        test_default -> Test with default arguments only.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.slave1 = SlaveRep("slave1", "20", True)
        self.slave2 = SlaveRep("slave2", "10", True)
        self.slave3 = SlaveRep("slave3", "15", True)
        self.slavearray = []
        self.slavearray2 = []
        self.slavearray.append(self.slave1)
        self.slavearray.append(self.slave2)
        self.slavearray.append(self.slave3)
        self.slavearray2.append(self.slave1)
        self.slaveorder = []
        self.slaveorder2 = []
        slv0 = self.slavearray[0]
        slv1 = self.slavearray[1]
        slv2 = self.slavearray[2]
        self.slaveorder.append((slv1.exe_gtidset, slv1))
        self.slaveorder.append((slv2.exe_gtidset, slv2))
        self.slaveorder.append((slv0.exe_gtidset, slv0))
        self.slaveorder2.append((slv1.exe_gtidset, slv1))
        self.args_array = {"-G": "slave1"}
        self.args_array2 = {"-G": "slave0"}
        self.results = \
            "Slaves: ['slave2', 'slave3'] that did not change to new master."
        self.results2 = "Slaves: ['slave2'] that did not change to new master."
        self.results3 = "Slave: slave0 was not found in slave array"

    @mock.patch("mysql_rep_failover.mysql_libs.switch_to_master")
    def test_one_failed_switch(self, mock_switch):

        """Function:  test_one_failed_switch

        Description:  Test with switch to new master failed for one slave.

        Arguments:

        """

        mock_switch.side_effect = [-1, 0]

        self.assertEqual(mysql_rep_failover.promote_designated_slave(
            self.slavearray, self.args_array), (True, self.results2))

    @mock.patch("mysql_rep_failover.mysql_libs.switch_to_master")
    def test_failed_all_switch(self, mock_switch):

        """Function:  test_failed_all_switch

        Description:  Test with switch to new master failed for all slaves.

        Arguments:

        """

        mock_switch.return_value = -1

        self.assertEqual(mysql_rep_failover.promote_designated_slave(
            self.slavearray, self.args_array), (True, self.results))

    @mock.patch("mysql_rep_failover.mysql_libs.switch_to_master")
    def test_slv_not_found(self, mock_switch):

        """Function:  test_slv_not_found

        Description:  Test with no master found in slave list.

        Arguments:

        """

        mock_switch.return_value = 0

        self.assertEqual(mysql_rep_failover.promote_designated_slave(
            self.slavearray, self.args_array2), (True, self.results3))

    @unittest.skip("Bug:  Stacktraces with no slaves in list")
    @mock.patch("mysql_rep_failover.mysql_libs.switch_to_master")
    def test_no_slave(self, mock_switch):

        """Function:  test_no_slave

        Description:  Test with only no slaves in list.

        Arguments:

        """

        mock_switch.return_value = 0

        self.assertEqual(mysql_rep_failover.promote_designated_slave(
            [], self.args_array), (False, None))

    @mock.patch("mysql_rep_failover.mysql_libs.switch_to_master")
    def test_one_slave(self, mock_switch):

        """Function:  test_one_slave

        Description:  Test with only one slave in list.

        Arguments:

        """

        mock_switch.return_value = 0

        self.assertEqual(mysql_rep_failover.promote_designated_slave(
            self.slavearray2, self.args_array), (False, None))

    @mock.patch("mysql_rep_failover.mysql_libs.switch_to_master")
    def test_default(self, mock_switch):

        """Function:  test_promote_designated_slave

        Description:  Test with default arguments only.

        Arguments:

        """

        mock_switch.return_value = 0

        self.assertEqual(mysql_rep_failover.promote_designated_slave(
            self.slavearray, self.args_array), (False, None))


if __name__ == "__main__":
    unittest.main()
