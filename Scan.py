#!/usr/bin/python3

import ipaddress
import concurrent.futures
from sys import exit as sys_exit
import Target as tg

class Scan ():
    
    def __init__(self, ip, silent, banner_mode, type, max_port=65535):
        self.silent = silent
        self.banner_mode = banner_mode
        self.type = type
        self.targets = {}
        self.max_port = max_port
        
        if self.type:
            self.ip = ip
            self.ping_sweep_launcher()
        else:
            self.ip = ip.split(":")[0]
            self.port_scan_launcher()

        
    def color_print(self, type, message):
        if type == 'w':
            return("\033[93m" + message + "\033[0m")
        elif type == 'e':
            return("\033[91m" + message + "\033[0m")
        elif type == 'g':
            return("\033[92m" + message + "\033[0m")
        elif type == 'i':
            return("\033[94m" + message + "\033[0m")
        else:
            raise ValueError("Invalid color type provided.")
        
        
    def print_starting_message(self, ip_net):
        if self.type:
            print("{}\nAddress to scan: {}\nNetmask: {}\nThere are {} addresses to scan".format("_"*50, ip_net.network_address, ip_net.netmask, ip_net.num_addresses))
            if ip_net.num_addresses < 254 :
                print("Using " + str(ip_net.num_addresses) + " threads"+ "_"*50, "\n")
                return concurrent.futures.ThreadPoolExecutor(ip_net.num_addresses)
            else:
                print("Using 254 thread to do so \n" +"_"*50, "\n")
                return concurrent.futures.ThreadPoolExecutor(254)
        else:
            print("{}\nAddress to scan: {}\nThere are {} ports to scan".format("_"*50, self.ip, self.max_port))
            if self.max_port < 254 :
                print("Using " + str(self.max_port) + " threads"+ "_"*50, "\n")
                return concurrent.futures.ThreadPoolExecutor(ip_net.num_addresses)
            else:
                print("Using 254 thread to do so \n" +"_"*50, "\n")
                return concurrent.futures.ThreadPoolExecutor(254)
        
        
    def ping_sweep_launcher(self):
        try:
            ip_net = ipaddress.ip_network(None)
        except ValueError:
            print(self.color_print("e","Invalid subnet. Please enter a valid subnet. the last bit need to be a zero"))
            return 1

        executor = self.print_starting_message(ip_net)

        # define the targets dict with the ip as key and the target object as value
        for ips in ip_net.hosts():
            self.targets[ips] = tg.Target(ips)

        ping = [executor.submit(self.targets[ips].test_connection) for ips in self.targets]
        concurrent.futures.wait(ping)
        for target in self.targets:
            if self.silent:
                if self.targets[target].status:
                    print( (str(self.targets[target].ip)) + self.color_print("g","\t[up]"))
            else:
                if self.targets[target].status:
                    print( (str(self.targets[target].ip)) + self.color_print("g","\t[up]"))
                else:
                    print( (str(self.targets[target].ip)) + self.color_print("e","\t[down]"))


    def print_open_ports(self, ports_data, port):
        print("Port {}".format(port) + self.color_print("g","\t\t[open]"))
        if self.banner_mode:
            print("Service: " + ports_data[port]["service"])
            print("Banner: " + ports_data[port]["banner"])


    def port_scan_launcher(self):
        try : 
            ip_net = ipaddress.ip_network(self.ip)
        except Exception: 
            print(self.color_print("e","Invalid IP address. Please enter a valid IP address."))
            sys_exit.exit(1)
            
        executor = self.print_starting_message(ip_net)
        self.targets[self.ip] = tg.Target(self.ip, self.max_port)

        self.targets[self.ip].scan_setup(self.banner_mode, self.silent, executor)
        ports_data = self.targets[self.ip].get_ports()
        
        for port in ports_data:
            if self.silent == False : 
                if ports_data[port]["state"]:
                    self.print_open_ports(ports_data, port)
            else:
                if ports_data[port]["state"] :
                    self.print_open_ports(ports_data, port)
                else:
                    print("Port {}".format(port) + self.color_print("e","\t\t[closed]"))
        
        print(self.color_print("i","Scan complete, {} ports scanned".format(self.max_port)))
