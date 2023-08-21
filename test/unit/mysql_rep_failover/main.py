# Classification (U)

"""Program:  main.py

    Description:  Unit testing of main in mysql_rep_failover.py.

    Usage:
        test/unit/mysql_rep_failover/main.py

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
import mysql_rep_failover
import lib.gen_libs as gen_libs
import version

__version__ = version.__version__


class ArgParser(object):

    """Class:  ArgParser

    Description:  Class stub holder for gen_class.ArgParser class.

    Methods:
        __init__
        arg_dir_chk
        arg_require
        get_val

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.cmdline = None
        self.args_array = dict()
        self.opt_req = None
        self.opt_req2 = True
        self.dir_perms_chk = None
        self.dir_perms_chk2 = True
        self.opt_xor_val = None
        self.opt_xor_val2 = True

    def arg_dir_chk(self, dir_perms_chk):

        """Method:  arg_dir_chk

        Description:  Method stub holder for gen_class.ArgParser.arg_dir_chk.

        Arguments:

        """

        self.dir_perms_chk = dir_perms_chk

        return self.dir_perms_chk2

    def arg_require(self, opt_req):

        """Method:  arg_require

        Description:  Method stub holder for gen_class.ArgParser.arg_require.

        Arguments:

        """

        self.opt_req = opt_req

        return self.opt_req2

    def arg_xor_dict(self, opt_xor_val):

        """Method:  arg_xor_dict

        Description:  Method stub holder for gen_class.ArgParser.arg_xor_dict.

        Arguments:

        """

        self.opt_xor_val = opt_xor_val

        return self.opt_xor_val2

    def get_val(self, skey, def_val=None):

        """Method:  get_val

        Description:  Method stub holder for gen_class.ArgParser.get_val.

        Arguments:

        """

        return self.args_array.get(skey, def_val)


class ProgramLock(object):

    """Class:  ProgramLock

    Description:  Class stub holder for gen_class.ProgramLock class.

    Methods:
        __init__

    """

    def __init__(self, cmdline, flavor):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:
            (input) cmdline
            (input) flavor

        """

        self.cmdline = cmdline
        self.flavor = flavor


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_programlock_id
        test_programlock_false
        test_programlock_true
        test_run_program
        test_arg_dir_chk_crt_true
        test_arg_dir_chk_crt_false
        test_arg_xor_dict_true
        test_arg_xor_dict_false
        test_arg_require_true
        test_arg_require_false
        test_help_false
        test_help_true

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.args = ArgParser()
        self.args2 = ArgParser()
        self.args.args_array = {"-c": "CfgFile", "-d": "CfgDir"}
        self.args2.args_array = {
            "-c": "CfgFile", "-d": "CfgDir", "-y": "Flavor"}
        self.proglock = ProgramLock(["cmdline"], "FlavorID")

    @mock.patch("mysql_rep_failover.run_program", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_failover.gen_class.ProgramLock")
    @mock.patch("mysql_rep_failover.gen_libs.help_func")
    @mock.patch("mysql_rep_failover.gen_class.ArgParser")
    def test_programlock_id(self, mock_arg, mock_help, mock_lock):

        """Function:  test_programlock_id

        Description:  Test with ProgramLock with flavor id.

        Arguments:

        """

        mock_arg.return_value = self.args2
        mock_help.return_value = False
        mock_lock.return_value = self.proglock

        self.assertFalse(mysql_rep_failover.main())

    @mock.patch("mysql_rep_failover.run_program", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_failover.gen_class.ProgramLock")
    @mock.patch("mysql_rep_failover.gen_libs.help_func")
    @mock.patch("mysql_rep_failover.gen_class.ArgParser")
    def test_programlock_false(self, mock_arg, mock_help, mock_lock):

        """Function:  test_programlock_false

        Description:  Test with ProgramLock returns False.

        Arguments:

        """

        mock_arg.return_value = self.args
        mock_help.return_value = False
        mock_lock.side_effect = \
            mysql_rep_failover.gen_class.SingleInstanceException

        with gen_libs.no_std_out():
            self.assertFalse(mysql_rep_failover.main())

    @mock.patch("mysql_rep_failover.run_program", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_failover.gen_class.ProgramLock")
    @mock.patch("mysql_rep_failover.gen_libs.help_func")
    @mock.patch("mysql_rep_failover.gen_class.ArgParser")
    def test_programlock_true(self, mock_arg, mock_help, mock_lock):

        """Function:  test_programlock_true

        Description:  Test with ProgramLock returns True.

        Arguments:

        """

        mock_arg.return_value = self.args
        mock_help.return_value = False
        mock_lock.return_value = self.proglock

        self.assertFalse(mysql_rep_failover.main())

    @mock.patch("mysql_rep_failover.run_program", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_failover.gen_class.ProgramLock")
    @mock.patch("mysql_rep_failover.gen_libs.help_func")
    @mock.patch("mysql_rep_failover.gen_class.ArgParser")
    def test_run_program(self, mock_arg, mock_help, mock_lock):

        """Function:  test_run_program

        Description:  Test with run_program.

        Arguments:

        """

        mock_arg.return_value = self.args
        mock_help.return_value = False
        mock_lock.return_value = self.proglock

        self.assertFalse(mysql_rep_failover.main())

    @mock.patch("mysql_rep_failover.run_program", mock.Mock(return_value=True))
    @mock.patch("mysql_rep_failover.gen_class.ProgramLock")
    @mock.patch("mysql_rep_failover.gen_libs.help_func")
    @mock.patch("mysql_rep_failover.gen_class.ArgParser")
    def test_arg_dir_chk_crt_true(self, mock_arg, mock_help, mock_lock):

        """Function:  test_arg_dir_chk_crt_true

        Description:  Test arg_dir_chk_crt if returns true.

        Arguments:

        """

        mock_arg.return_value = self.args
        mock_help.return_value = False
        mock_lock.return_value = self.proglock

        self.assertFalse(mysql_rep_failover.main())

    @mock.patch("mysql_rep_failover.gen_libs.help_func")
    @mock.patch("mysql_rep_failover.gen_class.ArgParser")
    def test_arg_dir_chk_crt_false(self, mock_arg, mock_help):

        """Function:  test_arg_dir_chk_crt_false

        Description:  Test arg_dir_chk_crt if returns false.

        Arguments:

        """

        self.args.dir_perms_chk2 = False

        mock_arg.return_value = self.args
        mock_help.return_value = False

        self.assertFalse(mysql_rep_failover.main())

    @mock.patch("mysql_rep_failover.gen_libs.help_func")
    @mock.patch("mysql_rep_failover.gen_class.ArgParser")
    def test_arg_xor_dict_true(self, mock_arg, mock_help):

        """Function:  test_arg_xor_dict_true

        Description:  Test arg_xor_dict if returns true.

        Arguments:

        """

        self.args.dir_perms_chk2 = False

        mock_arg.return_value = self.args
        mock_help.return_value = False

        self.assertFalse(mysql_rep_failover.main())

    @mock.patch("mysql_rep_failover.gen_libs.help_func")
    @mock.patch("mysql_rep_failover.gen_class.ArgParser")
    def test_arg_xor_dict_false(self, mock_arg, mock_help):

        """Function:  test_arg_xor_dict_false

        Description:  Test arg_xor_dict if returns false.

        Arguments:

        """

        self.args.opt_xor_val2 = False

        mock_arg.return_value = self.args
        mock_help.return_value = False

        self.assertFalse(mysql_rep_failover.main())

    @mock.patch("mysql_rep_failover.gen_libs.help_func")
    @mock.patch("mysql_rep_failover.gen_class.ArgParser")
    def test_arg_require_true(self, mock_arg, mock_help):

        """Function:  test_arg_require_true

        Description:  Test arg_require if returns true.

        Arguments:

        """

        self.args.opt_xor_val2 = False

        mock_arg.return_value = self.args
        mock_help.return_value = False

        self.assertFalse(mysql_rep_failover.main())

    @mock.patch("mysql_rep_failover.gen_libs.help_func")
    @mock.patch("mysql_rep_failover.gen_class.ArgParser")
    def test_arg_require_false(self, mock_arg, mock_help):

        """Function:  test_arg_require_false

        Description:  Test arg_require if returns false.

        Arguments:

        """

        self.args.opt_req2 = False

        mock_arg.return_value = self.args
        mock_help.return_value = False

        self.assertFalse(mysql_rep_failover.main())

    @mock.patch("mysql_rep_failover.gen_libs.help_func")
    @mock.patch("mysql_rep_failover.gen_class.ArgParser")
    def test_help_false(self, mock_arg, mock_help):

        """Function:  test_help_false

        Description:  Test help if returns false.

        Arguments:

        """

        self.args.opt_req2 = False

        mock_arg.return_value = self.args
        mock_help.return_value = False

        self.assertFalse(mysql_rep_failover.main())

    @mock.patch("mysql_rep_failover.gen_libs.help_func")
    @mock.patch("mysql_rep_failover.gen_class.ArgParser")
    def test_help_true(self, mock_arg, mock_help):

        """Function:  test_help_true

        Description:  Test help if returns true.

        Arguments:

        """

        mock_arg.return_value = self.args
        mock_help.return_value = True

        self.assertFalse(mysql_rep_failover.main())


if __name__ == "__main__":
    unittest.main()
