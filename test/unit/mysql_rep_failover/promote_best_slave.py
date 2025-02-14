# Classification (U)

"""Program:  promote_best_slave.py

    Description:  Unit testing of promote_best_slave in
        mysql_rep_failover.py.

    Usage:
        test/unit/mysql_rep_failover/promote_best_slave.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import unittest
import mock

# Local
sys.path.append(os.getcwd())
import mysql_rep_failover                       # pylint:disable=E0401,C0413
import version                                  # pylint:disable=E0401,C0413

__version__ = version.__version__


class ArgParser():                                      # pylint:disable=R0903

    """Class:  ArgParser

    Description:  Class stub holder for gen_class.ArgParser class.

    Methods:
        __init__

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.cmdline = None
        self.args_array = {}


class MasterRep():                                      # pylint:disable=R0903

    """Class:  MasterRep

    Description:  Class stub holder for mysql_class.MasterRep class.

    Methods:
        __init__

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.name = "MySQL_Name"
        self.conn_msg = None


class SlaveRep():

    """Class:  SlaveRep

    Description:  Class stub holder for mysql_class.SlaveRep class.

    Methods:
        __init__
        remove
        append

    """

    def __init__(self, name, exe_gtidset, gtid_mode):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:
            (input) name -> Name of instance.
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
            (input) master

        """

        self.master = master

        return True

    def append(self, slave):

        """Method:  append

        Description:  Stub holder for mysql_class.SlaveRep.append method.

        Arguments:
            (input) slave

        """

        self.slave = slave

        return True


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_failed_master
        test_one_failed_switch
        test_failed_all_switch
        test_one_slave
        test_default

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.args = ArgParser()
        self.args2 = ArgParser()
        self.args.args_array = {"-G": "slave1"}
        self.args2.args_array = {"-G": "slave0"}
        self.master = MasterRep()
        self.slave1 = SlaveRep("slave1", "20", True)
        self.slave2 = SlaveRep("slave2", "10", True)
        self.slave3 = SlaveRep("slave3", "15", True)
        self.slavearray = []
        self.slavearray2 = []
        self.slavearray.append(self.slave1)
        self.slavearray.append(self.slave2)
        self.slavearray.append(self.slave3)
        self.slavearray2.append(self.slave1)
        self.results = \
            "Slaves: ['slave3', 'slave1'] that did not change to new master."
        self.results2 = "Slaves: ['slave3'] that did not change to new master."
        self.results4 = \
            "promote_best_slave: Error on server MySQL_Name:  Error "
        self.results4 = self.results4 + "No slaves were changed to new master."

    @mock.patch("mysql_rep_failover.convert_to_master")
    def test_failed_master(self, mock_master):

        """Function:  test_failed_master

        Description:  Test with switch to new master failed for one slave.

        Arguments:

        """

        self.master.conn_msg = "Error"

        mock_master.return_value = self.master

        self.assertEqual(
            mysql_rep_failover.promote_best_slave(
                self.slavearray, self.args), (True, self.results4))

    @mock.patch("mysql_rep_failover.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_failover.convert_to_master",
                mock.Mock(return_value=MasterRep()))
    @mock.patch("mysql_rep_failover.mysql_libs.switch_to_master")
    def test_one_failed_switch(self, mock_switch):

        """Function:  test_one_failed_switch

        Description:  Test with switch to new master failed for one slave.

        Arguments:

        """

        mock_switch.side_effect = [-1, 0]

        self.assertEqual(
            mysql_rep_failover.promote_best_slave(
                self.slavearray, self.args), (True, self.results2))

    @mock.patch("mysql_rep_failover.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_failover.convert_to_master",
                mock.Mock(return_value=MasterRep()))
    @mock.patch("mysql_rep_failover.mysql_libs.switch_to_master")
    def test_failed_all_switch(self, mock_switch):

        """Function:  test_failed_all_switch

        Description:  Test with switch to new master failed for all slaves.

        Arguments:

        """

        mock_switch.return_value = -1

        self.assertEqual(
            mysql_rep_failover.promote_best_slave(
                self.slavearray, self.args), (True, self.results))

    @mock.patch("mysql_rep_failover.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_failover.convert_to_master",
                mock.Mock(return_value=MasterRep()))
    @mock.patch("mysql_rep_failover.mysql_libs.switch_to_master")
    def test_one_slave(self, mock_switch):

        """Function:  test_one_slave

        Description:  Test with only one slave in list.

        Arguments:

        """

        mock_switch.return_value = 0

        self.assertEqual(
            mysql_rep_failover.promote_best_slave(
                self.slavearray2, self.args), (False, None))

    @mock.patch("mysql_rep_failover.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_failover.convert_to_master",
                mock.Mock(return_value=MasterRep()))
    @mock.patch("mysql_rep_failover.mysql_libs.switch_to_master")
    def test_default(self, mock_switch):

        """Function:  test_promote_best_slave

        Description:  Test with default arguments only.

        Arguments:

        """

        mock_switch.return_value = 0

        self.assertEqual(
            mysql_rep_failover.promote_best_slave(
                self.slavearray, self.args), (False, None))


if __name__ == "__main__":
    unittest.main()
