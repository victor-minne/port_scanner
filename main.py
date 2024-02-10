#!/usr/bin/python3

import sys
import Scan as sc

def color_print(type, message):
    if type == 'w' :
        return("\033[93m" + message + "\033[0m")
    elif type == 'e' :
        return("\033[91m" + message + "\033[0m")
    elif type == 'g' :
        return("\033[92m" + message + "\033[0m")
    elif type == 'i' :
        return("\033[94m" + message + "\033[0m")


def print_help():
    print(color_print("w","Usage: python3 port_scanner.py <mode> <-h> <-v> <-b> <IP/hostname></netmask or :port>\n"))
    print("Modes:\n--ping_sweep or -ps to permform a ping sweep\n--port_scan or -s to scan a single target\n--help -h for this menu\n-v for verbose mode\n -b for banner grabbing\n")
    print("Example: python3 port_scanner.py --ping_sweep 192.168.100.0/24")
    print("Example: python3 port_scanner.py --port_scan 192.168.100.5:100\n")
    print(color_print("i","Note: \n>the last bit of the subnet need to be a zero\n>the port range need to be between 1 and 65535\n>the ip/hostname need to be the last argument\n"))
    sys.exit(1)
    
    
def print_usage ():
        print (color_print('w', "Missing arguments\nUsage: python3 port_scanner.py <mode> <-h> <-v> <IP/hostname></netmask or :port>\n"))
        sys.exit(1)
    
    
if __name__ == "__main__":
    # should manage only the argument parsing and call the right function

    if "-h" in sys.argv or "--help" in sys.argv:
        print_help()
        
    if len(sys.argv) < 3 :
        print_usage()
    
    # false means no verbose (silent mode)
    silent = True if "-v" in sys.argv else False 
    
    # True means ping_sweep, False means port_scan
    type = True if "--ping_sweep" in sys.argv or "-ps" in sys.argv else None
    type = False if "--port_scan" in sys.argv or "-s" in sys.argv else type
    if type == None : print_help()
    if type == False:
        max_port = int(sys.argv[-1].split(":")[1])
        if max_port > 65535 or max_port < 0:
            print(color_print("e","Invalid port range. Please enter a valid port range."))
            sys.exit(1)
    else:
        max_port = 65535
        
    banner_grabbing = True if "-b" in sys.argv else False
    ip = sys.argv[-1]
    
    scan = sc.Scan(ip, silent, banner_grabbing, type, max_port)
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
# 22. improve the arguments management, and the help menu
# 23. Done
