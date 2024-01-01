import ipaddress
import sys
import subprocess
import concurrent.futures


def print_help():
    print("Usage: python3 port_scanner.py <mode> <subnet/netmask> ")
    print("Modes:\n--ping_sweep or -ps\n--port_scan or -s")
    print("Example: python3 port_scanner.py --ping_sweep 192.168.100.0/24")
    sys.exit(1)


def ping_sweep (ip, silent=True):
    is_broadcast = ipaddress.ip_address(ip).is_global
    if not is_broadcast:
        try:
            subprocess.check_output(["ping", "-c", "1", ip])
            print("Found : ", ip)
            
        except Exception as exc:
            if not silent:             
                print(f"{ip} generated an exception: {exc}")
            

def port_scan (ip):
    # need to make the port scan according to the subnet and mask
    pass

try :
    if __name__ == "__main__":
        
        if "-h" in sys.argv or "--help" in sys.argv:
            print_help()
            
        
        if len(sys.argv) < 3 :
            print("Usage: python3 port_scanner.py <mode> <subnet/netmask> <-v> ")
            sys.exit(1)
            
        try:
            ip_net = ipaddress.ip_network(sys.argv[2])
        except ValueError:
            print("Invalid subnet. Please enter a valid subnet. the last bit need to be a zero")
            sys.exit(1)
            
        silent = False if "-v" in sys.argv else True
        
        if "--ping_sweep" in sys.argv or "-ps" in sys.argv:
            
            print("Address to scan :", ip_net.network_address)
            print("Netmask : ", ip_net.netmask)
            print("there are " + str(ip_net.num_addresses) + " addresses to scan")
            
            if ip_net.num_addresses < 254 :
                executor = concurrent.futures.ThreadPoolExecutor(ip_net.num_addresses)
                print("Using " + str(ip_net.num_addresses) + " threads")
            else:
                executor = concurrent.futures.ThreadPoolExecutor(254)
                
            hosts = ip_net.hosts()
            ping_hosts = [executor.submit(ping_sweep, str(ip), silent ) for ip in hosts]
        
        elif "--port_scan" in sys.argv or "-P" in sys.argv:
            # need to make the port scan according to the subnet and mask
            port_scan(ip_net.network_address)
            
        else : 
            print_help()
except KeyboardInterrupt:
        print("\n Interrupted by user. Exiting...")
        sys.exit()

# TODO:
# 1. make a port scanner
# 2. add an option ip ranges more than subnets
# 3. add an option to set the number of threads
# 4. add an option of file output
# 5. add an option of input file