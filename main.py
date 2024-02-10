#!/usr/bin/python3

import sys
import Scan as sc
import argparse

def color_print(type, message):
    if type == 'w' :
        return("\033[93m" + message + "\033[0m")
    elif type == 'e' :
        return("\033[91m" + message + "\033[0m")
    elif type == 'g' :
        return("\033[92m" + message + "\033[0m")
    elif type == 'i' :
        return("\033[94m" + message + "\033[0m")
    else:
        raise ValueError("Invalid color type provided.")
    
    
if __name__ == "__main__":
    # should manage only the argument parsing and call the right function

    parser = argparse.ArgumentParser(description='Port scanner')
    parser.add_argument('--ping_sweep', '-ps', action='store_true', help='Perform a ping sweep')
    parser.add_argument('--port_scan', '-s', action='store_true', help='Scan a single target')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose mode')
    parser.add_argument('--banner_grabbing', '-b', action='store_true', help='Banner grabbing')
    parser.add_argument('-ip', type=str, help='IP or hostname to scan')
    parser.add_argument('--port_range', "-p", type=int, help='Max port to scan')
    parser.add_argument('--net_mask', "-m", type=int, help='Subnet to scan')
    
    args = parser.parse_args()
    
    if args.ip == None:
        print(color_print("e","Missing arguments : IP"))
        parser.print_help()
        sys.exit(1)
    
    if args.port_range == False and args.net_mask == False:
        print(color_print("e","Missing arguments : port_range or net_mask"))
        parser.print_help()
        sys.exit(1)
    
    if args.port_range and args.net_mask:
        print(color_print("e","You can't use both port_range and net_mask at the same time"))
        parser.print_help()
        sys.exit(1)
    
    if args.ping_sweep == False and args.port_scan == False:
        print(color_print("e","You need to specify a mode (ping_sweep or port_scan)"))
        parser.print_help()
        sys.exit(1)
        
    if args.ping_sweep and args.port_scan:
        print(color_print("e","You can't use both ping_sweep and port_scan at the same time"))
        parser.print_help()
        sys.exit(1)
    
    
    if args.ping_sweep :
        # fais le ping_sweep
        type = True
        if args.net_mask == None:
            print(color_print("e","You need to specify a net_mask"))
            parser.print_help()
            sys.exit(1)
        if 0 > parser.net_mask < 32:
            print(color_print("e","Invalid net_mask. Please enter a valid net_mask."))
            parser.print_help()
            sys.exit(1)

    else:
        # fais le port_scan
        type = False
        if args.port_range == None:
            print(color_print("e","You need to specify a port_range"))
            parser.print_help()
            sys.exit(1)
        if -1 > args.port_range > 65536:
            print(color_print("e","Invalid port range. Please enter a valid port range. (1-65535)"))
            parser.print_help()
            sys.exit(1)
                
        banner_grabbing = False if args.banner_grabbing == None else True
        



    
    scan = sc.Scan(args.ip, args.verbose, banner_grabbing, type, args.port_range, args.net_mask)
    if type:
        scan.ping_sweep_launcher()
    else:
        scan.port_scan_launcher()
    sys.exit(0)







# see : https://gist.github.com/arnavdas88/dde5c8e3b436cc6db42792270034a94b
# 2. add an option ip ranges/list more than subnets
# 3. add an option to set the number of threads
# 4. add an option of file output
# 5. add an option of input file
# 7. add an option to set the ports to scan (precise not range)
# 9. add an option to set the timeout
# 10. add an option to set the number of retries
# 15. make an anonymous ftp login optional
# 16. for 80 and 443, add an option to get robots.txt and sitemap.xml
# 17. add an option to fuzz the webserver
# 18. add an option to list files in ftp server, and download them
# 19. add an option to list the users in the ftp server
# 20. add the same as FTP for SMB
# 21. add an option to automatically connect to a ssh server with a dictionnary, or anonymously
