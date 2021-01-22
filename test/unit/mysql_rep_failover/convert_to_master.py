#!/usr/bin/python
# Classification (U)

"""Program:  convert_to_master.py

    Description:  Unit testing of convert_to_master in mysql_rep_failover.py.

    Usage:
        test/unit/mysql_rep_failover/convert_to_master.py

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


class MasterRep(object):

    """Class:  MasterRep

    Description:  Class stub holder for mysql_class.MasterRep class.

    Methods:
        __init__ -> Class initialization.
        connect -> Stub holder for mysql_class.MasterRep.connect method.

    """

    def __init__(self, name, server_id, sql_user, sql_pass, machine, **kwargs):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:
            (input) name -> Name of instance.
            (input) server_id -> Server ID.
            (input) sql_user -> Sql user name.
            (input) sql_pass -> SQL user pswd.
            (input) machine -> Machine instance.
            (input) kwargs:
                host -> Host name.
                port -> SQL port.
                defaults_file -> Defaults file name.
                extra_def_file -> Extra defaults file name.
                rep_user -> Replication user name.
                rep_japd -> Replication user pswd.

        """

        self.name = name
        self.server_id = server_id
        self.sql_user = sql_user
        self.sql_pass = sql_pass
        self.machine = machine
        self.host = kwargs.get("host", "localhost")
        self.port = kwargs.get("port", 3306)
        self.defaults_file = kwargs.get("defaults_file", None)
        self.extra_def_file = kwargs.get("extra_def_file", None)
        self.rep_user = kwargs.get("rep_user", None)
        self.rep_japd = kwargs.get("rep_japd", None)

    def connect(self):

        """Method:  connect

        Description:  Stub holder for mysql_class.MasterRep.connect method.

        Arguments:

        """

        return True


class SlaveRep(object):

    """Class:  SlaveRep

    Description:  Class stub holder for mysql_class.SlaveRep class.

    Methods:
        __init__ -> Class initialization.

    """

    def __init__(self, name, server_id, sql_user, sql_pass, machine, **kwargs):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:
            (input) name -> Name of instance.
            (input) server_id -> Server ID.
            (input) sql_user -> Sql user name.
            (input) sql_pass -> SQL user pswd.
            (input) machine -> Machine instance.
            (input) kwargs:
                host -> Host name.
                port -> SQL port.
                defaults_file -> Defaults file name.
                extra_def_file -> Extra defaults file name.

        """

        self.name = name
        self.server_id = server_id
        self.sql_user = sql_user
        self.sql_pass = sql_pass
        self.machine = machine
        self.host = kwargs.get("host", "localhost")
        self.port = kwargs.get("port", 3306)
        self.defaults_file = kwargs.get("defaults_file", None)
        self.extra_def_file = kwargs.get("extra_def_file", None)


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_default -> Test with default arguments only.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        name = "MySQLName"
        server_id = 10
        sql_user = "sqluser"
        sql_pass = "sqljapd"
        machine = "Linux"
        host = "Hostname"
        port = 3306
        defaults_file = "DefaultsFileName"
        extra_def_file = "ExtraDefFileName"
        rep_user = "Replication user name"
        rep_japd = "Replication user pswd"

        self.slave = SlaveRep(
            name, server_id, sql_user, sql_pass, machine, host=host,
            port=port, defaults_file=defaults_file,
            extra_def_file=extra_def_file)
        self.master = MasterRep(
            self.slave.name, self.slave.server_id, self.slave.sql_user,
            self.slave.sql_pass, self.slave.machine, host=self.slave.host,
            port=self.slave.port, defaults_file=self.slave.defaults_file,
            extra_def_file=self.slave.extra_def_file, rep_user=rep_user,
            rep_japd=rep_japd)
        self.args_array = {"-s": "slavefile", "-d": "configdir"}
        self.slv_array = {"name": name, "port": port, "rep_user": rep_user,
                          "rep_japd": rep_japd}

    @mock.patch("mysql_rep_failover.mysql_class.MasterRep")
    @mock.patch("mysql_rep_failover.cmds_gen.create_cfg_array")
    def test_default(self, mock_array, mock_master):

        """Function:  test_promote_best_slave

        Description:  Test with default arguments only.

        Arguments:

        """

        mock_array.return_value = [self.slv_array]
        mock_master.return_value = self.master

        master = mysql_rep_failover.convert_to_master(self.slave,
                                                      self.args_array)

        self.assertTrue(isinstance(master, MasterRep))


if __name__ == "__main__":
    unittest.main()
