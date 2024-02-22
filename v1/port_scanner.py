#!/usr/bin/python3

import ipaddress
import sys
import subprocess
import concurrent.futures
import socket


def print_help():
    print(color_print("w","Usage: python3 port_scanner.py <mode> <-h> <-v> <-b> <IP/hostname></netmask or :port>\n"))
    print("Modes:\n--ping_sweep or -ps to permform a ping sweep\n--port_scan or -s to scan a single target\n--help -h for this menu\n-v for verbose mode\n -b for banner grabbing\n")
    print("Example: python3 port_scanner.py --ping_sweep 192.168.100.0/24")
    print("Example: python3 port_scanner.py --port_scan 192.168.100.5:100\n")
    print(color_print("i","Note: \n>the last bit of the subnet need to be a zero\n>the port range need to be between 1 and 65535\n>the ip/hostname need to be the last argument\n"))
    sys.exit(1)


def ping_test_connection (ip, silent=True):
    try:
        subprocess.check_output(["ping", "-c", "1", ip])
        if not silent : 
            print("Connection established with :", ip)
        return True

    except KeyboardInterrupt:
        print("\nExiting program.")
        sys.exit()

    except Exception as exc:
        print("enable to connect to " + ip + " : " + str(exc))
        return False


def ping_sweep (ip, silent=True):
    is_broadcast = ipaddress.ip_address(ip).is_global # is_global return True if the ip is a broadcast address 
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
            

def anonymous_ftp_login (s):
    s.sendall(b"USER anonymous\r\n")
    user = s.recv(1024)
    s.sendall(b"PASS anonymous\r\n")
    password = s.recv(1024)
    return user + "\n" + password


def banner_grabbing_func (s, ports):
    try:
        if ports == 80:
            s.sendall(b"HEAD / HTTP/1.1\r\n\r\n")
            banner = s.recv(1024)
            
            """elif service == "smtp":
                    banner = smartDecode(s.recv(1024))
                    total_communication = banner + "\r\n"
                elif service == "ssh":
                    banner = smartDecode(s.recv(1024))
                    total_communication = banner
                elif service == "pop3":
                    banner = smartDecode(s.recv(1024))
                    s.send(b"USER root\r\n")
                    user = smartDecode(s.recv(1024))
                    s.send(b"PASS root\r\n")
                    password = smartDecode(s.recv(1024))
                    total_communication = banner +  "\r\n" + user + "\r\n" + password
            """
        elif ports == 21:
            banner = s.recv(1024)
            total_communication = banner + anonymous_ftp_login(s)
            print('> ' + total_communication.decode())
        else :                 
            s.sendall("")
            banner = s.recv(1024)
            if banner.isempty():
                s.sendall(b'WhoAreYou\r\n')
                banner = s.recv(1024)
        # need to add an empty char to send and try to receive the banner, but need to be dependant of the port scanned (http, ftp, ssh, etc.)
        
        print('> ' + banner.decode())
    except:
        print("> Cannot grab banner\n")


def scan (ip, ports, silent=True, banner_grabbing=False):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(1)
    result = s.connect_ex((ip,ports))
    if result == 0:
        print("Port {}".format(ports) + color_print("g","\t[open]"))
        if banner_grabbing: banner_grabbing_func(s, ports)
        
    else:
        if not silent:
            print("Port {}".format(ports) + color_print("e","\t[closed]"))
    s.close()


def port_scan (ip, ports, silent=True, banner_grabbing=False):
    if ping_test_connection(ip):
        try:
            scan(ip, ports, silent, banner_grabbing)

        except KeyboardInterrupt:
            print("\nExiting program.")
            sys.exit()

        except TimeoutError:
            print("TimeoutError")
            return "TimeoutError"

        except socket.gaierror as e:
            print(color_print(e,"Hostname could not be resolved."))
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


def launching_ping_sweep(silent) :
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


def launching_port_scan (silent, banner_grabbing):
    if not silent:
        print("starting port scan")
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

    scan_host = [executor.submit(port_scan, ip , ports, silent, banner_grabbing) for ports in max_port]
    concurrent.futures.wait(scan_host)
    print(color_print("i","Scan complete, {} ports scanned".format(len(max_port))))


def print_usage ():
        print (color_print('w', "Missing arguments\nUsage: python3 port_scanner.py <mode> <-h> <-v> <IP/hostname></netmask or :port>\n"))
        sys.exit(1)


if __name__ == "__main__":
    
    if "-h" in sys.argv or "--help" in sys.argv:
        print_help()
        
    if len(sys.argv) < 3 :
        print_usage()

    silent = False if "-v" in sys.argv else True
    
    if "--ping_sweep" in sys.argv or "-ps" in sys.argv:
        launching_ping_sweep(silent)

    elif "--port_scan" in sys.argv or "-P" in sys.argv:
        banner_grabbing = True if "-b" in sys.argv else False
        launching_port_scan(silent, banner_grabbing)

    else : 
        print_help()


