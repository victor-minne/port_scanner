#!/usr/bin/python3

from sys import exit
import Scan as sc
from argparse import ArgumentParser
from os import path

def color_print(color, message):
    """
    Prints the given message in the specified color type.

    Parameters:
    - type (str): The color type. Valid values are 'w' (warning), 'e' (error), 'g' (success), 'i' (info).
    - message (str): The message to be printed.

    Returns:
    - str: The formatted message with the specified color.

    Raises:
    - ValueError: If an invalid color type is provided.
    """
    match color:
        case 'w':
            return("\033[93m" + message + "\033[0m")
        case 'e':
            return("\033[91m" + message + "\033[0m")
        case 'g':
            return("\033[92m" + message + "\033[0m")
        case 'i':
            return("\033[94m" + message + "\033[0m")
        case _:
            raise ValueError("Invalid color type provided.")

def list_exploits():
    from os import listdir
    from os.path import isfile, join
    exploits_path = path.dirname(path.abspath(__file__)) + "/res/exploit_script"
    onlyfiles = [f for f in listdir(exploits_path) if isfile(join(exploits_path, f))]
    for file in onlyfiles :
        print(file.split(".")[0])
        
def init_banner(arguments) :
    return False if arguments.banner_grabbing == None else True

def init_scan_type(arguments) :
    if arguments.ping_sweep == False and arguments.port_scan == False:
        print(color_print("e","You need to specify a mode (ping_sweep or port_scan)"))
        parser.print_help()
        exit(1)
        
    if arguments.ping_sweep and arguments.port_scan:
        print(color_print("e","You can't use both ping_sweep and port_scan at the same time"))
        parser.print_help()
        exit(1)
        
    
    if arguments.ping_sweep :
        # fais le ping_sweep
        scan_type = True
        if arguments.net_mask == None:
            print(color_print("e","You need to specify a net_mask"))
            parser.print_help()
            exit(1)
        if 0 > arguments.net_mask < 32:
            print(color_print("e","Invalid net_mask. Please enter a valid net_mask."))
            parser.print_help()
            exit(1)

    else  :
        # fais le port_scan
        scan_type = False
        if arguments.port_range == None:
            print(color_print("e","You need to specify a port_range"))
            parser.print_help()
            exit(1)
        if -1 > arguments.port_range > 65536:
            print(color_print("e","Invalid port range. Please enter a valid port range. (1-65535)"))
            parser.print_help()
            exit(1)
    return scan_type

def init_timeout(arguments) :
    if arguments.timeout == None:
        return 1
    return arguments.timeout
    
def init_threads(arguments) :
    if arguments.threads == None:
        return 254
    return arguments.threads
        
def init_args (arguments): 
    
    if arguments.ls == True:
        list_exploits()
        exit(0)
    
    if arguments.ip == None:
        print(color_print("e","Missing arguments : IP"))
        parser.print_help()
        exit(1)
    
    if arguments.port_range == False and arguments.net_mask == False:
        print(color_print("e","Missing arguments : port_range or net_mask"))
        parser.print_help()
        exit(1)
    
    if arguments.port_range and arguments.net_mask:
        print(color_print("e","You can't use both port_range and net_mask at the same time"))
        parser.print_help()
        exit(1)
    
    
    
    # need to be modify so it's not a argument of the command but more 
    # of an exploit script or something, can be part of an -A command for example 
    # that tries multiple things.
    if arguments.pull == None:
        arguments.pull = False
    else :
        # check that the path is valid
        if arguments.pull[-1] != "/":
            arguments.pull += "/"
        if not path.exists(arguments.pull):
            parser.print_help()
            print(color_print("e","Invalid path. Please enter a valid path."))
            exit(1)
    
    if arguments.script != None :
        if arguments.script[-1] == "/" :
            parser.print_help()
            print(color_print("e", "Please provide a file and not a directory."))
            exit(1)
        else :
            # check if path exist 
            if not path.exist(exploit_folder + "/" + arguments.script + ".py"):
                parser.print_help()
                print(color_print("e", "Script not found, try to check the name of the script with "))
                exit(1)


if __name__ == "__main__":
    
    exploit_folder = path.dirname(path.abspath(__file__)) + "/res/exploit_script"

    parser = ArgumentParser(description='Port scanner')
    parser.add_argument('--ping_sweep', '-ps', action='store_true', help='Perform a ping sweep')
    parser.add_argument('--port_scan', '-s', action='store_true', help='Scan a single target')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose mode')
    parser.add_argument('--banner_grabbing', '-b', action='store_true', help='Banner grabbing')
    parser.add_argument('-ip', type=str, help='IP or hostname to scan')
    parser.add_argument('--port_range', "-p", type=int, help='Max port to scan')
    parser.add_argument('--net_mask', "-m", type=int, help='Subnet to scan')
    parser.add_argument('--timeout', "-t", type=int, help='Timeout for the scan, the time is an INT in seconds')
    parser.add_argument('--threads', "-th", type=int, help='Number of threads to use, will be limited to the number of ports if you set more thread than ports')
    parser.add_argument('--pull', "-pl", type=str, help='Pull files from the FTP server, need to precise the path to where you want to place them')
    parser.add_argument('--script', '-sc', type=str, help='name of the script you want to use, available script are in the /res/exploit folder. You can also view them using --lssc')
    parser.add_argument('-ls', action='store_true', help='list exploit scripts available. You can view the /res/explpoit folder too see a direct view of them.')
    arguments = parser.parse_args()
    
    init_args(arguments)
    banner_grabbing = init_banner(arguments)
    scan_type = init_scan_type(arguments)
    timeout= init_timeout(arguments)
    threads = init_threads(arguments)
    scan = sc.Scan(arguments.ip, arguments.verbose, banner_grabbing, scan_type, arguments.port_range, arguments.net_mask, timeout, threads, arguments.pull, arguments.script)
    if scan_type:
        scan.ping_sweep_launcher()
    else:
        scan.port_scan_launcher()
    exit(0)


# need an option to run multiple scripts
# imports can be done conditionnaly and in method/function or class to improve the performance
# see : https://gist.github.com/arnavdas88/dde5c8e3b436cc6db42792270034a94b
# 2. add an option ip ranges/list more than subnets
# 7. add an option to set the ports to scan (precise not range)         
# 15. make an anonymous ftp login optional                              // need to make a module for connections/enums scripts 
# 4. add an option of file output
# 5. add an option of input file (for ip list, port list)               // -ipf option and a path then we loop through the file.
# 17. add an option to fuzz the webserver (lightly)                              // need to add it in an appart module
# 20. add the same as FTP for SMB
# 21. add an option to automatically connect to a ssh server with a dictionnary, or anonymously
