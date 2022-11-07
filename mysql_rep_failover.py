#!/usr/bin/python
# Classification (U)

"""Program:  mysql_rep_failover.py

    Description:  Administration program for MySQL Replication system.  The
        program has a number of functions to allow the failover of a
        replication system from a master to a slave.  This failover can be done
        to the best slave possible or a designed slave.  The program can also
        be used to show the best slave in a slave replication set and show the
        differences between the slaves in the replication set.  This program is
        assuming that the master is down or otherwise unavailable and will not
        require a master replication configuration file, only a slave
        configuration file.

    NOTE:  This program will allow the changing of the slaves databases to new
        replication configurations, but it does not update the slave
        configuration file or creates a new master configuration file.  This is
        done outside the scope of this program.

    Usage:
        mysql_rep_failover.py -s [path]file -d path
            {-F |
             -G name |
             -B |
             -D}
            [-y flavor_id] [-v | -h]

    Arguments:
        -s [path/]file => Slave config file.  Will be a text file.  Include the
            file extension with the name.  Can include the path or use the -d
            option path.  Required arg.
        -d dir path => Directory path to the config files. Required arg.

        -F => Select the best slave within the replication set and promote it
            to master and make all other slaves change to the new master.

        -G name => Take the designated name of the slave and promote it
            to master and make all other slaves change to the new master.
            WARNING:  This option could result in loss of transactions
                in the replication set as this option will override the best
                slave promotion and could possibly make a slave which is
                behind the rest of the slaves a master database.

        -B => Displays the name of the current best slave in the
            replication set based on it's current positions compared
            with the other slaves in the set.

        -D => Shows the slaves in the replication set from best to
            worst and displays the differences.

        -y value => A flavor id for the program lock.  To create unique lock.
        -v => Display version of this program.
        -h => Help and usage message.

        NOTE 1:  -v or -h overrides the other options.
        NOTE 2:  -F, -G, -B, and -D are XOR arguments.

    Notes:
        Slave configuration file format (config/slave.txt.TEMPLATE)
            # Slave configuration
            user = USER
            japd = PASSWORD
            rep_user = REP_USER
            rep_japd = REP_PSWORD
            host = HOST_IP
            name = HOST_NAME
            sid = SERVER_ID
            cfg_file = None
            port = 3306
            serv_os = Linux
            extra_def_file = PYTHON_PROJECT/mysql.cfg

            # If SSL connections are being used, configure one or more of these
                entries:
            ssl_client_ca = None
            ssl_client_key = None
            ssl_client_cert = None

            # Only changes these if necessary and have knowledge in MySQL
                SSL configuration setup:
            ssl_client_flag = None
            ssl_disabled = False
            ssl_verify_id = False
            ssl_verify_cert = False

            # Set what TLS versions are allowed in the connection set up:
            tls_versions = []

        NOTE 1:  Include the cfg_file even if running remotely as the file will
            be used in future releases.
        NOTE 2:  In MySQL 5.6 - it now gives warning if password is passed on
            the command line.  To suppress this warning, will require the use
            of the --defaults-extra-file option (i.e. extra_def_file) in the
            database configuration file.  See below for the defaults-extra-file
            format.
        NOTE 3:  The rep_user entry is the name of the Replication user that is
            used across the replication domain.

        Defaults Extra File format (config/mysql.cfg.TEMPLATE):
            [client]
            password="PSWORD"
            socket="DIRECTORY_PATH/mysqld.sock"

        NOTE 1:  The socket information can be obtained from the my.cnf
            file under ~/mysql directory.
        NOTE 2:  The --defaults-extra-file option will be overridden if there
            is a ~/.my.cnf or ~/.mylogin.cnf file located in the home directory
            of the user running this program.  The extras file will in effect
            be ignored.
        NOTE 3:  Socket use is only required to be set in certain conditions
            when connecting using localhost.

    Example:
        mysql_rep_failover.py -s slaves.txt -d config -F

"""

# Libraries and Global Variables

# Standard
import sys

# Local
try:
    from .lib import arg_parser
    from .lib import gen_libs
    from .lib import gen_class
    from .mysql_lib import mysql_libs
    from .mysql_lib import mysql_class
    from . import version

except (ValueError, ImportError) as err:
    import lib.arg_parser as arg_parser
    import lib.gen_libs as gen_libs
    import lib.gen_class as gen_class
    import mysql_lib.mysql_libs as mysql_libs
    import mysql_lib.mysql_class as mysql_class
    import version

__version__ = version.__version__


def help_message():

    """Function:  help_message

    Description:  Displays the program's docstring which is the help and usage
        message when -h option is selected.

    Arguments:

    """

    print(__doc__)


def show_slave_delays(slaves, args_array, **kwargs):

    """Function:  show_slave_delays

    Description:  Display the best slave followed by the next best slaves and
        their GTID positions.

    Arguments:
        (input) slaves -> Slave instance array.
        (input) args_array -> Array of command line options and values.
        (input) kwargs:
            slv_key -> Dictionary of keys and data types.
        (output) err_flag -> True|False - if an error has occurred.
        (output) err_msg -> Error message.

    """

    err_flag = False
    err_msg = None
    args_array = dict(args_array)
    slaves = list(slaves)
    slave_list = order_slaves_on_gtid(slaves)
    gtid, slv = slave_list.pop(0)
    print("Best Slave: {0}\tGTID Pos: {1}".format(slv.name, gtid))

    for gtid, slv in slave_list:
        print("     Slave: {0}\tGTID Pos: {1}".format(slv.name, gtid))

    return err_flag, err_msg


def show_best_slave(slaves, args_array, **kwargs):

    """Function:  show_best_slave

    Description:  Display which slave is the best slave within the replication.

    Arguments:
        (input) slaves -> Slave instance array.
        (input) args_array -> Array of command line options and values.
        (input) kwargs:
            slv_key -> Dictionary of keys and data types.
        (output) err_flag -> True|False - if an error has occurred.
        (output) err_msg -> Error message.

    """

    err_flag = False
    err_msg = None
    args_array = dict(args_array)
    slaves = list(slaves)
    _, best_slv = order_slaves_on_gtid(slaves).pop(0)
    print("Best Slave: %s" % (best_slv.name))

    return err_flag, err_msg


def promote_designated_slave(slaves, args_array, **kwargs):

    """Function:  promote_designated_slave

    Description:  Promote a designated slave to the new master.  It will then
        change all of the other slaves in the replication set to point
        to the new master.

    NOTE:  No change to the slave thread on the new master is done.  This
        thread will still point to the old master.

    Arguments:
        (input) slaves -> Slave instance array.
        (input) args_array -> Array of command line options and values.
        (input) kwargs:
            slv_key -> Dictionary of keys and data types.
        (output) err_flag -> True|False - if an error has occurred.
        (output) err_msg -> Error message.

    """

    args_array = dict(args_array)
    slaves = list(slaves)
    err_flag = False
    err_msg = None
    bad_slv = []
    new_master = mysql_libs.find_name(slaves, args_array["-G"])

    if new_master:
        slaves.remove(new_master)
        master = convert_to_master(new_master, args_array, **kwargs)

        if master.conn_msg:
            err_flag = True
            err_msg = "promote_designated_slave: Error on server(%s):  %s " % \
                (master.name, master.conn_msg)
            err_msg = err_msg + "No slaves were changed to new master."

        else:
            for slv in slaves:
                status_flag = mysql_libs.switch_to_master(master, slv)

                if status_flag == -1:
                    err_flag = True
                    bad_slv.append(slv.name)

            if err_flag:
                err_msg = "Slaves: %s that did not change to new master." \
                        % (bad_slv)

            mysql_libs.disconnect(master)

    else:
        err_flag = True
        err_msg = "Slave: %s was not found in slave array" % (args_array["-G"])

    return err_flag, err_msg


def order_slaves_on_gtid(slaves):

    """Function:  order_slaves_on_gtid

    Description:  Take a Slave array and sort them on their GTID positions,
        with the top(first) slave being the best Slave.

    Arguments:
        (input) slaves -> Slave instance array.
        (output) slave_list -> List of slaves in best order.

    """

    slaves = list(slaves)
    slave_list = []

    for slv in slaves:
        slave_list.append((slv.exe_gtidset, slv))

    slave_list.sort(key=lambda item: item[0])

    return slave_list


def convert_to_master(slave, args_array, **kwargs):

    """Function:  convert_to_master

    Description:  Creates MasterRep instance from a SlaveRep instance.

    Arguments:
        (input) slaves -> Slave instance array.
        (input) args_array -> Array of command line options and values.
        (input) kwargs:
            slv_key -> Dictionary of keys and data types.
        (output) master -> MasterRep instance.

    """

    slv_array = gen_libs.create_cfg_array(args_array["-s"],
                                          cfg_path=args_array["-d"])
    slv_array = gen_libs.transpose_dict(slv_array, kwargs.get("slv_key", {}))

    for entry in slv_array:
        if slave.name == entry["name"] and slave.port == int(entry["port"]):
            rep_user = entry["rep_user"]
            rep_japd = entry["rep_japd"]
            break

    master = mysql_class.MasterRep(
        slave.name, slave.server_id, slave.sql_user, slave.sql_pass,
        slave.machine, host=slave.host, port=slave.port,
        defaults_file=slave.defaults_file, extra_def_file=slave.extra_def_file,
        rep_user=rep_user, rep_japd=rep_japd)
    master.connect()

    return master


def promote_best_slave(slaves, args_array, **kwargs):

    """Function:  promote_best_slave

    Description:  Finds the best slave within the replication set and promotes
        it to the new master.  It will then change all of the other slaves
        in the replication set to point to the new master.

    NOTE:  No change to the slave thread on the new master is done.  This
         thread will still point to the old master.

    Arguments:
        (input) slaves -> Slave instance array.
        (input) args_array -> Array of command line options and values.
        (input) kwargs:
            slv_key -> Dictionary of keys and data types.
        (output) err_flag -> True|False - if an error has occurred.
        (output) err_msg -> Error message.

    """

    args_array = dict(args_array)
    slaves = list(slaves)
    err_flag = False
    err_msg = None
    bad_slv = []
    slave_list = order_slaves_on_gtid(slaves)

    # Best slave (new master) will be at the top.
    _, new_master = slave_list.pop(0)
    master = convert_to_master(new_master, args_array, **kwargs)

    if master.conn_msg:
        err_flag = True
        err_msg = "promote_best_slave: Error on server(%s):  %s " % \
            (master.name, master.conn_msg)
        err_msg = err_msg + "No slaves were changed to new master."

    else:
        for _, slv in slave_list:
            status_flag = mysql_libs.switch_to_master(master, slv)

            if status_flag == -1:
                err_flag = True
                bad_slv.append(slv.name)

        if err_flag:
            err_msg = "Slaves: %s that did not change to new master." % \
                      (bad_slv)

        mysql_libs.disconnect(master)

    return err_flag, err_msg


def create_instances(args_array, **kwargs):

    """Function:  create_instances

    Description:  Create SlaveRep instances for the slaves.  The slave
        instances will be appended to an array.

    Arguments:
        (input) args_array -> Array of command line options and values.
        (input) kwargs:
            slv_key -> Dictionary of keys and data types.
        (output) slaves -> List of slave instances.

    """

    args_array = dict(args_array)
    slaves = []

    # Parse the slave config file.
    slv_array = gen_libs.create_cfg_array(args_array["-s"],
                                          cfg_path=args_array["-d"])
    slv_array = gen_libs.transpose_dict(slv_array, kwargs.get("slv_key", {}))
    slaves = mysql_libs.create_slv_array(slv_array)

    return slaves


def gtid_enabled(slaves):

    """Function:  gtid_enabled

    Description:  Check to see that all slaves are GTID enabled.

    Arguments:
        (input) slaves -> Slave instance array.
        (output) is_enabled -> True|False - If all slaves are GTID enabled.

    """

    slaves = list(slaves)
    is_enabled = True

    for slv in slaves:
        if not slv.gtid_mode:
            is_enabled = False

    return is_enabled


def run_program(args_array, func_dict, **kwargs):

    """Function:  run_program

    Description:  Creates class instance(s) and controls flow of the program.

    Arguments:
        (input) args_array -> Array of command line options and values.
        (input) func_dict -> Dictionary list of functions and options.
        (input) kwargs:
            slv_key -> Dictionary of keys and data types.

    """

    args_array = dict(args_array)
    func_dict = dict(func_dict)
    slaves = create_instances(args_array, **kwargs)

    if slaves and gtid_enabled(slaves):

        # Call function(s) - intersection of command line and function dict.
        for item in set(args_array.keys()) & set(func_dict.keys()):
            err_flag, err_msg = func_dict[item](slaves, args_array, **kwargs)

            if err_flag:
                print(err_msg)
                break

        mysql_libs.disconnect(slaves)

    else:
        print("Error:  Empty Slave array or Slave(s) not GTID enabled.")


def main():

    """Function:  main

    Description:  Initializes program-wide used variables and processes command
        line arguments and values.

    Variables:
        dir_chk_list -> contains options which will be directories.
        func_dict -> dictionary list for the function calls or other options.
        opt_req_list -> contains the options that are required for the program.
        opt_val_list -> contains options which require values.
        opt_xor_dict -> contains dict with key that is xor with it's values.
        slv_key -> contains dict with keys to be converted to data types.

    Arguments:
        (input) argv -> Arguments from the command line.

    """

    cmdline = gen_libs.get_inst(sys)
    dir_chk_list = ["-d"]
    func_dict = {"-B": show_best_slave, "-D": show_slave_delays,
                 "-F": promote_best_slave, "-G": promote_designated_slave}
    opt_req_list = ["-d", "-s"]
    opt_val_list = ["-d", "-s", "-G", "-y"]
    opt_xor_dict = {"-B": ["-D", "-F", "-G"], "-D": ["-B", "-F", "-G"],
                    "-F": ["-B", "-D", "-G"], "-G": ["-B", "-D", "-F"]}
    slv_key = {"sid": "int", "port": "int", "cfg_file": "None",
               "ssl_client_ca": "None", "ssl_ca_path": "None",
               "ssl_client_key": "None", "ssl_client_cert": "None",
               "ssl_client_flag": "int", "ssl_disabled": "bool",
               "ssl_verify_id": "bool", "ssl_verify_cert": "bool"}

    # Process argument list from command line.
    args_array = arg_parser.arg_parse2(cmdline.argv, opt_val_list)

    if not gen_libs.help_func(args_array, __version__, help_message) \
       and not arg_parser.arg_require(args_array, opt_req_list) \
       and arg_parser.arg_xor_dict(args_array, opt_xor_dict) \
       and not arg_parser.arg_dir_chk_crt(args_array, dir_chk_list):

        try:
            prog_lock = gen_class.ProgramLock(cmdline.argv,
                                              args_array.get("-y", ""))
            run_program(args_array, func_dict, slv_key=slv_key)
            del prog_lock

        except gen_class.SingleInstanceException:
            print("WARNING:  Lock in place for mysql_rep_failover with id: %s"
                  % (args_array.get("-y", "")))


if __name__ == "__main__":
    sys.exit(main())
