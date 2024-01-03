#!/usr/bin/python3

import ipaddress
import sys
import subprocess
import concurrent.futures
import socket


def print_help():
    print(color_print("w","Usage: python3 port_scanner.py <mode> <-h> <-v> <IP/hostname></netmask or :port>\n"))
    print("Modes:\n--ping_sweep or -ps to permform a ping sweep\n--port_scan or -s to scan a single target\n--help -h for this menu\n-v for verbose mode\n")
    print("Example: python3 port_scanner.py --ping_sweep 192.168.100.0/24")
    print("Example: python3 port_scanner.py --port_scan 192.168.100.5:100\n")
    print(color_print("i","Note: \n>the last bit of the subnet need to be a zero\n>the port range need to be between 1 and 65535\n>the ip/hostname need to be the last argument\n"))
    sys.exit(1)


def ping_sweep (ip, silent=True):
    is_broadcast = ipaddress.ip_address(ip).is_global
    if not is_broadcast:
        try:
            subprocess.check_output(["ping", "-c", "1", ip])
            print("Found : ", ip)
        
        except KeyboardInterrupt:
            print("\nExiting program.")
            sys.exit()
            
        except Exception as exc:
            if not silent:             
                print(f"{ip} generated an exception: {exc}")
            

def port_scan (ip, ports, silent=True):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = s.connect_ex((ip,ports))
        if result == 0:
            print("Port {}".format(ports) + color_print("g","\t[open]"))
            try:
                s.sendall(b'WhoAreYou\r\n')
                banner = s.recv(1024)
                print('> ' + banner.decode())
            except:
                print("> Cannot grab banner\n")
        else:
            if not silent:
                print("Port {}".format(ports) + color_print("e","\t[closed]"))
        s.close()

    except KeyboardInterrupt:
        print("\nExiting program.")
        sys.exit()
        
    except socket.gaierror:
        print(color_print("e","Hostname could not be resolved."))
        sys.exit()


def color_print(type, message):
    if type == 'w' :
        return("\033[93m" + message + "\033[0m")
    elif type == 'e' :
        return("\033[91m" + message + "\033[0m")
    elif type == 'g' :
        return("\033[92m" + message + "\033[0m")
    elif type == 'i' :
        return("\033[94m" + message + "\033[0m")

if __name__ == "__main__":
    
    if "-h" in sys.argv or "--help" in sys.argv:
        print_help()
        
    if len(sys.argv) < 3 :
        print (color_print('w', "Missing arguments\nUsage: python3 port_scanner.py <mode> <-h> <-v> <IP/hostname></netmask or :port>\n"))
        sys.exit(1)
        
    silent = False if "-v" in sys.argv else True
    
    if "--ping_sweep" in sys.argv or "-ps" in sys.argv:
        
        try:
            ip_net = ipaddress.ip_network(sys.argv[-1])
        except ValueError:
            print(color_print("e","Invalid subnet. Please enter a valid subnet. the last bit need to be a zero"))
            sys.exit(1)
        
        print("{}\nAddress to scan: {}\nNetmask: {}\nThere are {} addresses to scan".format("_"*50, ip_net.network_address, ip_net.netmask, ip_net.num_addresses))
        if ip_net.num_addresses < 254 :
            executor = concurrent.futures.ThreadPoolExecutor(ip_net.num_addresses)
            print("Using " + str(ip_net.num_addresses) + " threads"+ "_"*50, "\n")
        else:
            executor = concurrent.futures.ThreadPoolExecutor(254)
            print("_"*50, "\n")

        ping_hosts = [executor.submit(ping_sweep, str(ip), silent ) for ip in ip_net.hosts()]
        concurrent.futures.wait(ping_hosts)
        print(color_print("i","Scan complete, {} hosts responded".format(len(ping_hosts))))
    
    elif "--port_scan" in sys.argv or "-P" in sys.argv:
        
        ip = socket.gethostbyname(sys.argv[-1].split(":")[0])    
        max_port = range(0, int(sys.argv[-1].split(":")[1]), 1)
        
        if int(sys.argv[-1].split(":")[1]) > 65535 or int(sys.argv[-1].split(":")[1]) < 1:
            print(color_print("e","Invalid port range. Please enter a valid port range."))
            sys.exit(1)
        
        print("_"*50, "\nAddress to scan :" + ip + "\nport : 1-", len(max_port))
        
        if len(max_port) < 254 :
            executor = concurrent.futures.ThreadPoolExecutor(max_port[-1])
            print("Using " + str(max_port) + " threads\n" + "_"*50 + "\n")
        else:
            executor = concurrent.futures.ThreadPoolExecutor(254)
            print("Using 254 threads (default value) \n" + "_"*50 + "\n")

        scan_host = [executor.submit(port_scan, ip , ports, silent) for ports in max_port]
        concurrent.futures.wait(scan_host)
        print(color_print("i","Scan complete, {} ports scanned".format(len(max_port))))
        
    else : 
        print_help()



# TODO:
# 2. add an option ip ranges/list more than subnets
# 3. add an option to set the number of threads
# 4. add an option of file output
# 5. add an option of input file
# 7. add an option to set the ports to scan (precise not range)
# 9. add an option to set the timeout
# 10. add an option to set the number of retries
# 13. add an option to enable or disable the banner grabbing 
# 14. check if ip is reachable before scanning
# 15. improve banner grabbing to vary the message send based on the port scanned
