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

    WARNING:  This program will allow the changing of the slaves databases to
        new replication configurations, but it does not update the
        slave configuration files or creates new master configuration
        files.  This must be done outside the scope of this program.

    Usage:
        mysql_rep_failover.py -s [path/]file -d path [-F | -G name | -B | -D]
        [-v | -h]

    Arguments:
        -s file => Slave config file.  Will be a text file.  Include the
            file extension with the name.  Can include the path or use
            the -d option path.  Required arg.
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
        -v => Display version of this program.
        -h => Help and usage message.

        NOTE 1:  -v or -h overrides the other options.
        NOTE 2:  -F, -G, -B, and -D are XOR arguments.

    Notes:
        Slave configuration file format (slave.txt.TEMPLATE)
            # Slave configuration
            user = root
            passwd = ROOT_PASSWORD
            host = IP_ADDRESS
            serv_os = Linux or Solaris
            name = HOSTNAME
            port = PORT_NUMBER
            cfg_file DIRECTORY_PATH/my.cnf
            sid = SERVER_ID
            extra_def_file = DIRECTORY_PATH/mysql.cfg

        NOTE 1:  Include the cfg_file even if running remotely as the file will
            be used in future releases.

        NOTE 2:  In MySQL 5.6 - it now gives warning if password is passed on
            the command line.  To suppress this warning, will require the use
            of the --defaults-extra-file option (i.e. extra_def_file) in the
            database configuration file.  See below for the defaults-extra-file
            format.

        Defaults Extra File format (mysql.cfg.TEMPLATE):
            [client]
            password="ROOT_PASSWORD"
            socket="DIRECTORY_PATH/mysql.sock"

        NOTE:  The socket information can be obtained from the my.cnf
            file under ~/mysql directory.

    Example:
        mysql_rep_failover.py -s slaves.txt -d config -F

"""

# Libraries and Global Variables

# Standard
import sys

# Local
import lib.arg_parser as arg_parser
import lib.gen_libs as gen_libs
import lib.cmds_gen as cmds_gen
import mysql_lib.mysql_libs as mysql_libs
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
        (output) True|False -> if an error has occurred.
        (output) -> Error message.

    """

    slave_list = order_slaves_on_gtid(slaves)

    gtid, slv = slave_list.pop(0)
    print("Best Slave: {0}\tGTID Pos: {1}".format(slv.name, gtid))

    for gtid, slv in slave_list:
        print("\tSlave: {0}\tGTID Pos: {1}".format(slv.name, gtid))

    return False, None


def show_best_slave(slaves, args_array, **kwargs):

    """Function:  show_best_slave

    Description:  Display which slave is the best slave within the replication.

    Arguments:
        (input) slaves -> Slave instance array.
        (input) args_array -> Array of command line options and values.
        (output) True|False -> if an error has occurred.
        (output) -> Error message.

    """

    __, best_slv = order_slaves_on_gtid(slaves).pop(0)
    print("Best Slave: %s" % (best_slv.name))

    return False, None


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
        (output) err_flag -> True|False - if an error has occurred.
        (output) err_msg -> Error message.

    """

    args_array = dict(args_array)
    slaves = list(slaves)
    err_flag = False
    err_msg = None
    bad_slv = []
    master = mysql_libs.find_name(slaves, args_array["-G"])

    if master:
        slaves.remove(master)

        for slv in slaves:
            status_flag = mysql_libs.switch_to_master(master, slv)

            if status_flag == -1:
                err_flag = True
                bad_slv.append(slv.name)

        if err_flag:
            err_msg = "Slaves: %s that did not change to new master." \
                      % (bad_slv)

    else:
        err_flag = True
        err_msg = "Slave: %s was not found in slave array" % (master.name)

    return err_flag, err_msg


def order_slaves_on_gtid(slaves, **kwargs):

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

    slave_list.sort(key=lambda x: x[0])

    return slave_list


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
    __, master = slave_list.pop(0)

    for __, slv in slave_list:
        status_flag = mysql_libs.switch_to_master(master, slv)

        if status_flag == -1:
            err_flag = True
            bad_slv.append(slv.name)

    if err_flag:
        err_msg = "Slaves: %s that did not change to new master." % (bad_slv)

    return err_flag, err_msg


def create_instances(args_array, **kwargs):

    """Function:  create_instances

    Description:  Create SlaveRep instances for the slaves.  The slave
        instances will be appended to an array.

    Arguments:
        (input) args_array -> Array of command line options and values.
        (output) SLAVE -> Slave instance array.

    """

    args_array = dict(args_array)
    slaves = []

    # Parse the slave config file.
    slv_array = cmds_gen.create_cfg_array(args_array["-s"],
                                          cfg_path=args_array["-d"])
    slaves = mysql_libs.create_slv_array(slv_array)

    return slaves


def gtid_enabled(slaves, **kwargs):

    """Function:  gtid_enabled

    Description:  Check to see that all slaves are GTID enabled.

    Arguments:
        (input) slaves -> Slave instance array.
        (output) True|False - If all slaves are GTID enabled.

    """

    slaves = list(slaves)
    gtid_enabled = True

    for slv in slaves:
        if not slv.gtid_mode:
            gtid_enabled = False

    return gtid_enabled


def run_program(args_array, func_dict, **kwargs):

    """Function:  run_program

    Description:  Creates class instance(s) and controls flow of the program.

    Arguments:
        (input) args_array -> Array of command line options and values.
        (input) func_dict -> Dictionary list of functions and options.

    """

    args_array = dict(args_array)
    func_dict = dict(func_dict)
    slaves = create_instances(args_array)

    if slaves and gtid_enabled(slaves):

        # Call function(s) - intersection of command line and function dict.
        for x in set(args_array.keys()) & set(func_dict.keys()):
            err_flag, err_msg = func_dict[x](slaves, args_array)

            if err_flag:
                cmds_gen.disconnect(slaves)
                sys.exit(err_msg)
                break

        cmds_gen.disconnect(slaves)

    else:
        sys.exit("Error:  Empty Slave array or Slave(s) not GTID enabled.")


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

    Arguments:
        (input) argv -> Arguments from the command line.

    """

    dir_chk_list = ["-d"]
    func_dict = {"-B": show_best_slave, "-D": show_slave_delays,
                 "-F": promote_best_slave, "-G": promote_designated_slave}
    opt_req_list = ["-d", "-s"]
    opt_val_list = ["-d", "-s", "-G"]
    opt_xor_dict = {"-B": ["-D", "-F", "-G"], "-D": ["-B", "-F", "-G"],
                    "-F": ["-B", "-D", "-G"], "-G": ["-B", "-D", "-F"]}

    # Process argument list from command line.
    args_array = arg_parser.arg_parse2(sys.argv, opt_val_list)

    if not gen_libs.help_func(args_array, __version__, help_message) \
       and not arg_parser.arg_require(args_array, opt_req_list) \
       and arg_parser.arg_xor_dict(args_array, opt_xor_dict) \
       and not arg_parser.arg_dir_chk_crt(args_array, dir_chk_list):
        run_program(args_array, func_dict)


if __name__ == "__main__":
    sys.exit(main())
