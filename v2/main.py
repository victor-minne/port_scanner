#!/usr/bin/python3

from sys import exit
from Scan import Scan as sc
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
    
    
if __name__ == "__main__":

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
    
    args = parser.parse_args()
    
    if args.ip == None:
        print(color_print("e","Missing arguments : IP"))
        parser.print_help()
        exit(1)
    
    if args.port_range == False and args.net_mask == False:
        print(color_print("e","Missing arguments : port_range or net_mask"))
        parser.print_help()
        exit(1)
    
    if args.port_range and args.net_mask:
        print(color_print("e","You can't use both port_range and net_mask at the same time"))
        parser.print_help()
        exit(1)
    
    if args.ping_sweep == False and args.port_scan == False:
        print(color_print("e","You need to specify a mode (ping_sweep or port_scan)"))
        parser.print_help()
        exit(1)
        
    if args.ping_sweep and args.port_scan:
        print(color_print("e","You can't use both ping_sweep and port_scan at the same time"))
        parser.print_help()
        exit(1)
    
    
    if args.ping_sweep :
        # fais le ping_sweep
        type = True
        if args.net_mask == None:
            print(color_print("e","You need to specify a net_mask"))
            parser.print_help()
            exit(1)
        if 0 > args.net_mask < 32:
            print(color_print("e","Invalid net_mask. Please enter a valid net_mask."))
            parser.print_help()
            exit(1)

    else:
        # fais le port_scan
        type = False
        if args.port_range == None:
            print(color_print("e","You need to specify a port_range"))
            parser.print_help()
            exit(1)
        if -1 > args.port_range > 65536:
            print(color_print("e","Invalid port range. Please enter a valid port range. (1-65535)"))
            parser.print_help()
            exit(1)
                
    banner_grabbing = False if args.banner_grabbing == None else True
        
        
    if args.timeout == None:
        timeout = 1
        
    if args.threads == None:
        threads = 254
    
    if args.pull == None:
        args.pull = False
    else :
        # check that the path is valid
        if args.pull[-1] != "/":
            args.pull += "/"
        if not path.exists(args.pull):
            print(color_print("e","Invalid path. Please enter a valid path."))
            parser.print_help()
            exit(1)
        
        
    
    scan = sc.Scan(args.ip, args.verbose, banner_grabbing, type, args.port_range, args.net_mask, args.timeout, args.threads, args.pull)
    if type:
        scan.ping_sweep_launcher()
    else:
        scan.port_scan_launcher()
    exit(0)



# imports can be done conditionnaly and in method/function or class to improve the performance
# see : https://gist.github.com/arnavdas88/dde5c8e3b436cc6db42792270034a94b
# 2. add an option ip ranges/list more than subnets
# 7. add an option to set the ports to scan (precise not range)         
# 15. make an anonymous ftp login optional                              // need to make a module for connections/enums scripts 
# 4. add an option of file output
# 5. add an option of input file
# 10. add an option to set the number of retries
# 17. add an option to fuzz the webserver                               // need to add it in an appart module
# 19. add an option to list the users in the ftp server                 // need to add it in an appart module
# 20. add the same as FTP for SMB
# 21. add an option to automatically connect to a ssh server with a dictionnary, or anonymously
