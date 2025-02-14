# Classification (U)

"""Program:  order_slaves_on_gtid.py

    Description:  Unit testing of order_slaves_on_gtid in
        mysql_rep_failover.py.

    Usage:
        test/unit/mysql_rep_failover/order_slaves_on_gtid.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import unittest

# Local
sys.path.append(os.getcwd())
import mysql_rep_failover                       # pylint:disable=E0401,C0413
import version                                  # pylint:disable=E0401,C0413

__version__ = version.__version__


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
            (input) name
            (input) exe_gtidset
            (input) gtid_mode

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
        test_no_slave
        test_one_slave
        test_default

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
        self.slaveorder2.append((slv0.exe_gtidset, slv0))

    def test_no_slave(self):

        """Function:  test_no_slave

        Description:  Test with only no slaves in list.

        Arguments:

        """

        self.assertEqual(mysql_rep_failover.order_slaves_on_gtid([]), [])

    def test_one_slave(self):

        """Function:  test_one_slave

        Description:  Test with only one slave in list.

        Arguments:

        """

        self.assertEqual(mysql_rep_failover.order_slaves_on_gtid(
            self.slavearray2), self.slaveorder2)

    def test_default(self):

        """Function:  test_order_slaves_on_gtid

        Description:  Test with default arguments only.

        Arguments:

        """

        self.assertEqual(mysql_rep_failover.order_slaves_on_gtid(
            self.slavearray), self.slaveorder)


if __name__ == "__main__":
    unittest.main()
