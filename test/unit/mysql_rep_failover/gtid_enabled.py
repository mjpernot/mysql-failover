#!/usr/bin/python
# Classification (U)

"""Program:  gtid_enabled.py

    Description:  Unit testing of gtid_enabled in
        mysql_rep_failover.py.

    Usage:
        test/unit/mysql_rep_failover/gtid_enabled.py

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

    def remove(self, master):

        """Method:  remove

        Description:  Stub holder for mysql_class.SlaveRep.remove method.

        Arguments:
            (input) master -> Master name.

        """

        return True

    def append(self, slave):

        """Method:  append

        Description:  Stub holder for mysql_class.SlaveRep.append method.

        Arguments:
            (input) slave -> Slave name.

        """

        return True


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_gtid_not_enabled -> Test with gtid not enabled.
        test_gtid_enabled -> Test with gtid enabled.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.slave1 = SlaveRep("slave1", "20", True)
        self.slave2 = SlaveRep("slave2", "10", True)
        self.slave3 = SlaveRep("slave3", "15", True)
        self.slave4 = SlaveRep("slave4", "25", False)
        self.slavearray = []
        self.slavearray.append(self.slave1)
        self.slavearray.append(self.slave2)
        self.slavearray.append(self.slave3)
        self.slavearray2 = []
        self.slavearray2.append(self.slave1)
        self.slavearray2.append(self.slave2)
        self.slavearray2.append(self.slave3)
        self.slavearray2.append(self.slave4)

    def test_gtid_not_enabled(self):

        """Function:  test_gtid_not_enabled

        Description:  Test with gtid not enabled.

        Arguments:

        """

        self.assertFalse(mysql_rep_failover.gtid_enabled(self.slavearray2))

    def test_gtid_enabled(self):

        """Function:  test_gtid_enabled

        Description:  Test with gtid enabled.

        Arguments:

        """

        self.assertTrue(mysql_rep_failover.gtid_enabled(self.slavearray))


if __name__ == "__main__":
    unittest.main()
