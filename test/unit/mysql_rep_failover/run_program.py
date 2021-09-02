#!/usr/bin/python
# Classification (U)

"""Program:  run_program.py

    Description:  Unit testing of run_program in mysql_rep_failover.py.

    Usage:
        test/unit/mysql_rep_failover/run_program.py

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


def show_slave_delays(slaves, args_array):

    """Method:  show_slave_delays

    Description:  Stub holder for mysql_rep_failover.show_slave_delays func.

    Arguments:
        (input) slaves -> List of slave connections.
        (input) args_array -> Array of command line options and values.

    """

    status = True

    if slaves and args_array:
        status = True

    return status, "Error Message"


def show_best_slave(slaves, args_array):

    """Method:  show_best_slave

    Description:  Stub holder for mysql_rep_failover.show_best_slave function.

    Arguments:
        (input) slaves -> List of slave connections.
        (input) args_array -> Array of command line options and values.

    """

    status = False

    if slaves and args_array:
        status = False

    return status, None


class SlaveRep(object):

    """Class:  SlaveRep

    Description:  Class stub holder for mysql_class.SlaveRep class.

    Methods:
        __init__ -> Class initialization.

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


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_function_fails -> Test with function failing.
        test_not_gtid_enabled -> Test with gtid not enabled.
        test_no_slaves -> Test with no slaves in list.
        test_run_program -> Test with only default arguments passed.

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
        self.slavearray.append(self.slave1)
        self.slavearray.append(self.slave2)
        self.slavearray.append(self.slave3)
        self.func_dict = {"-B": show_best_slave}
        self.func_dict2 = {"-D": show_slave_delays}
        self.args_array = {"-B": True}
        self.args_array2 = {"-D": True}

    @mock.patch("mysql_rep_failover.gtid_enabled",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_failover.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_failover.create_instances")
    def test_function_fails(self, mock_instance):

        """Function:  test_function_fails

        Description:  Test with function failing.

        Arguments:

        """

        mock_instance.return_value = self.slavearray

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_failover.run_program(self.args_array2,
                                                            self.func_dict2))

    @mock.patch("mysql_rep_failover.gtid_enabled",
                mock.Mock(return_value=False))
    @mock.patch("mysql_rep_failover.create_instances")
    def test_not_gtid_enabled(self, mock_instance):

        """Function:  test_not_gtid_enabled

        Description:  Test with gtid not enabled.

        Arguments:

        """

        mock_instance.return_value = self.slavearray

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_failover.run_program(self.args_array,
                                                            self.func_dict))

    @mock.patch("mysql_rep_failover.gtid_enabled",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_failover.create_instances")
    def test_no_slaves(self, mock_instance):

        """Function:  test_no_slaves

        Description:  Test with no slaves in list.

        Arguments:

        """

        mock_instance.return_value = []

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_failover.run_program(self.args_array,
                                                            self.func_dict))

    @mock.patch("mysql_rep_failover.gtid_enabled",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_failover.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_rep_failover.create_instances")
    def test_run_program(self, mock_instance):

        """Function:  test_run_program

        Description:  Test with only default arguments passed.

        Arguments:

        """

        mock_instance.return_value = self.slavearray

        self.assertFalse(mysql_rep_failover.run_program(self.args_array,
                                                        self.func_dict))


if __name__ == "__main__":
    unittest.main()
