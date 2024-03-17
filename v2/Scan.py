#!/usr/bin/python3

from datetime import datetime
from ipaddress import ip_network
from sys import exit as sys_exit
from main import color_print
import Target as tg
import concurrent.futures

class Scan ():
    
    def __init__(self, ip, silent, banner_mode, type, max_port=65535, net_mask=32, timeout=1, threads=254, pull=False, script=False):
        """
        Initialize the Scan object.

        Parameters:
        - ip (str): The IP address or hostname or IP range to scan.
        - silent (bool): Flag indicating if verbose mode is enabled.
        - banner_mode (bool): Flag indicating whether to retrieve banners for open ports.
        - type (bool): Flag indicating the type of scan to perform (True for ping sweep, False for port scan).
        - max_port (int): The maximum port number to scan (default is 65535).
        - net_mask (int): The network mask for the IP range (default is 32).

        Returns:
        None
        """
        self.silent = not silent
        self.banner_mode = banner_mode
        self.type = type
        self.targets = {}
        self.max_port = max_port
        self.net_mask = net_mask
        self.timeout = timeout
        self.threads = threads
        self.pull = pull
        
        if self.type:
            self.ip = ip + "/" + str(self.net_mask)
        else:
            self.ip = ip
        self.script = script

        
    # to improve we exec really similar code in both if + function is doing too much (print + set up the thread pool executor) should be done in 2 different functions)
    def print_starting_message(self, ip_net):
        """
        Prints the starting message for the port scanner and respond with the number of thread to use.

        Args:
            ip_net (ipaddress.IPv4Network): The IP network to scan.

        Returns:
            concurrent.futures.ThreadPoolExecutor: The thread pool executor object.

        """
        if self.type:
            print("{}\nAddress to scan: {}\nNetmask: {}\nThere are {} addresses to scan".format("_"*50, ip_net.network_address, ip_net.netmask, ip_net.num_addresses))
            if ip_net.num_addresses < self.threads :
                print("Using " + str(ip_net.num_addresses) + " threads"+ "_"*50, "\n")
                print(f"Port Scanner starting at: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
                print("_"*50, "\n")
                return concurrent.futures.ThreadPoolExecutor(ip_net.num_addresses)
            print("Using 254 thread to do so \n" +"_"*50, "\n")
            print(f"Port Scanner starting at: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            print("_"*50, "\n")
            return concurrent.futures.ThreadPoolExecutor(254)

        print("{}\nAddress to scan: {}\nThere are {} ports to scan".format("_"*50, self.ip, self.max_port))
        if self.max_port < self.threads :
            print("Using " + str(self.max_port) + " threads"+ "_"*50, "\n")
            print(f"Port Scanner starting at: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            print("_"*50, "\n")
            return concurrent.futures.ThreadPoolExecutor(ip_net.num_addresses)
        print("Using 254 thread to do so \n" +"_"*50, "\n")
        print(f"Port Scanner starting at: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print("_"*50, "\n")
        return concurrent.futures.ThreadPoolExecutor(self.threads)
        
        
    def ping_sweep_launcher(self):
        """
        Launches a ping sweep by testing the connection to each IP address in the specified subnet.

        Returns:
            int: 1 if an invalid subnet is provided, otherwise None.
        """
        try:
            ip_net = ip_network(self.ip)
        except ValueError:
            print(color_print("e","Invalid subnet. Please enter a valid subnet. the last bit need to be a zero"))
            return 1

        executor = self.print_starting_message(ip_net)

        # define the targets dict with the ip as key and the target object as value
        for ips in ip_net.hosts():
            self.targets[ips] = tg.Target(ips, self.timeout)

        # problem comes from the next line
        ping = [executor.submit(self.targets[ips].test_connection) for ips in self.targets]
        concurrent.futures.wait(ping)
        for target in self.targets:
            if self.targets[target].status:
                print( (str(self.targets[target].ip)) + color_print("g","\t[up]"))
                continue
            if not self.silent:
                print( (str(self.targets[target].ip)) + color_print("e","\t[down]"))


    def print_open_ports(self, ports_data, port):
        """
        Prints information about an open port.

        Args:
            ports_data (dict): A dictionary containing port information.
            port (int): The port number.

        Returns:
            None
        """
        print("Port {}".format(port) + color_print("g","\t\t[open]"))
        if self.banner_mode:
            print("Service: " + ports_data[port]["service"])
            print("Banner: " + ports_data[port]["banner"])


    def port_scan_launcher(self):
        """
        Launches the port scanning process.

        This method performs the following steps:
        1. Validates the IP address provided.
        2. Call the prints starting message function.
        3. Create a target object for the specified IP address.
        4. Retrieves the ports data.
        5. Prints the retrieved data        # need to check that after

        Returns:
            None
        """
        try : 
            ip_net = ip_network(self.ip)
        except Exception: 
            print(color_print("e","Invalid IP address. Please enter a valid IP address."))
            sys_exit.exit(1)
            
        executor = self.print_starting_message(ip_net)
        self.targets[self.ip] = tg.Target(self.ip, self.max_port, self.timeout, self.threads)

        self.targets[self.ip].scan_setup(self.banner_mode, executor)
        self.print_result()
            
            
            
    def print_result(self):
            """
            Prints the scan results including the hostname and the state of each port.
            """
            ports_data = self.targets[self.ip].get_ports()
            hostname = self.targets[self.ip].get_hostname()
            if hostname != "":
                print("hostname : " + color_print("i", hostname))
            for port in ports_data:
                if ports_data[port]["state"]:
                    self.print_open_ports(ports_data, port)
                    continue
                if not self.silent:
                    print("Port {}".format(port) + color_print("e", "\t\t[closed]"))

            print(color_print("i", "Scan complete, {} ports scanned".format(self.max_port)))
