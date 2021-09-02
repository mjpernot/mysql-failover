#!/usr/bin/python
# Classification (U)

"""Program:  create_instances.py

    Description:  Unit testing of create_instances in
        mysql_rep_failover.py.

    Usage:
        test/unit/mysql_rep_failover/create_instances.py

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
        test_no_slave -> Test with no slaves in list.
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
        self.slavearray.append(self.slave1)
        self.slavearray.append(self.slave2)
        self.slavearray.append(self.slave3)
        self.args_array = {"-s": "CfgFile", "-d": "CfgDir"}

    @mock.patch("mysql_rep_failover.gen_libs.transpose_dict")
    @mock.patch("mysql_rep_failover.mysql_libs.create_slv_array")
    @mock.patch("mysql_rep_failover.gen_libs.create_cfg_array")
    def test_no_slave(self, mock_cfg, mock_slv, mock_trans):

        """Function:  test_no_slave

        Description:  Test with no slaves in list.

        Arguments:

        """

        mock_cfg.return_value = []
        mock_slv.return_value = []
        mock_trans.return_value = []

        self.assertEqual(mysql_rep_failover.create_instances(
            self.args_array), [])

    @mock.patch("mysql_rep_failover.gen_libs.transpose_dict")
    @mock.patch("mysql_rep_failover.mysql_libs.create_slv_array")
    @mock.patch("mysql_rep_failover.gen_libs.create_cfg_array")
    def test_default(self, mock_cfg, mock_slv, mock_trans):

        """Function:  test_default

        Description:  Test with default arguments only.

        Arguments:

        """

        mock_cfg.return_value = self.slavearray
        mock_slv.return_value = self.slavearray
        mock_trans.return_value = []

        self.assertEqual(mysql_rep_failover.create_instances(
            self.args_array), self.slavearray)


if __name__ == "__main__":
    unittest.main()
