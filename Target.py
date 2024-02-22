import concurrent
import ipaddress
import socket
import subprocess


class Target (): 
    """
    Represents a target for port scanning.

    Attributes:
    - ip (str): The IP address of the target.
    - hostname (str): The hostname of the target (empty if can't be found).
    - status (bool): The status of the target (False by default).
    - users (dict): A dictionary of users associated with the target (empty by default).
    - max_port (int): The maximum port number to scan.
    - ports (dict): A dictionary of ports and their status (False by default).
    """

    def __init__(self, ip, port=65535, timeout=1, threads=1, pull=False):
        """
        Initializes a Target object.

        Parameters:
        - ip (str): The IP address of the target.
        - port (int): The maximum port number to scan (default is 65535).
        """
        self.ip = ip
        self.hostname = ""
        self.status = False
        self.users = {}
        self.max_port = port
        self.ports = {}
        for port in range(1, self.max_port + 1):
            self.set_ports(port, False)
        self.set_hostname()
        self.timeout = timeout
        self.thread = threads
        self.pull = pull
        
    def get_ip(self):
        """
        Returns the IP address of the target.

        Returns:
        - str: The IP address of the target.
        """
        return self.ip
    
    def set_ip(self, ip):
        """
        Sets the IP address of the target.

        Parameters:
        - ip (str): The IP address to set.
        """
        self.ip = ip
        
    def get_hostname(self):
        """
        Returns the hostname of the target.

        Returns:
        - str: The hostname of the target.
        """
        return self.hostname
    
    def set_hostname(self):
        """
        Sets the hostname of the target based on its IP address.
        If the hostname cannot be resolved, an empty string is assigned.
        """
        try:
            self.hostname = socket.gethostbyaddr(self.ip)[0]
        except Exception:
            print("No hostname available")
            self.hostname = ""
    
    def get_status(self):
        """
        Returns the status of the target.

        Returns:
        - bool: The status of the target.
        """
        return self.status

    def set_status(self, status):
        """
        Sets the status of the target.

        Parameters:
        - status (bool): The status to set.
        """
        self.status = status
    
    def get_ports(self):
        """
        Returns the dictionary of ports and their status.

        Returns:
        - dict: A dictionary of ports and their status.
        """
        return self.ports
    
    def set_ports(self, port, state, service="", banner=""):
        """
        Sets the status, service, and banner for a specific port.

        Parameters:
        - port (int): The port number.
        - state (bool): The status of the port.
        - service (str): The service associated with the port (empty by default).
        - banner (str): The banner associated with the port (empty by default).
        """
        self.ports[port] = {"state": state, "service": service, "banner": banner}
    
    def get_users(self):
        """
        Returns the dictionary of users associated with the target.

        Returns:
        - dict: A dictionary of users associated with the target.
        """
        return self.users
    
    def set_users(self, user):
        """
        Adds a user to the dictionary of users associated with the target.

        Parameters:
        - user (str): The user to add.
        """
        self.users.append(user)
    
    def test_connection (self):
        """
        Tests the connection to the target by pinging it.

        If the target is reachable, sets the status to True. Otherwise, sets the status to False.
        """
        if not ipaddress.ip_address(self.ip).is_global:
            try:
                target = socket.gethostbyname(str(self.ip))
                subprocess.check_output(["ping", "-c", self.timeout, target])
                self.set_status(True)

            except Exception :
                self.set_status(False)
                
    def scanning(self, port, banner_mode):
        """
        Scans a specific port on the target.

        Parameters:
        - port (int): The port number to scan.
        - banner_mode (bool): Whether to perform banner grabbing for the port.
        - silent (bool): Whether to print output during scanning.
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(self.timeout)
        result = s.connect_ex((self.ip,port))
        
        if result == 0:
            self.set_ports(port, True)
            if banner_mode: 
                self.banner_grabbing(s, port)
        else:
            self.ports[port] = {"state": False, "service": "", "banner": ""}
        s.close()
    
    def scan_setup(self, banner_mode, executor):
        """
        Sets up the port scanning process.

        Parameters:
        - banner_mode (bool): Whether to perform banner grabbing for each port.
        - silent (bool): Whether to print output during scanning.
        - executor: The executor to use for concurrent scanning.
        """
        self.test_connection()
        scan_host = [executor.submit(self.scanning, port, banner_mode) for port in range(0, self.max_port, 1)]
        concurrent.futures.wait(scan_host)     
     

    def banner_grabbing(self, s, port):
        """
        Performs banner grabbing for a specific port.

        Parameters:
        - s: The socket object.
        - port (int): The port number.
        """
        try:
            if port == 80:
                s.sendall(b"HEAD / HTTP/1.1\r\n\r\n")
                banner = s.recv(1024)
                
                self.ports[port]["banner"] = banner.decode()
            elif port == 21:
                import ftp_scripts
                self.ports[port]["banner"] = ftp_scripts.ftp_connect(self.ip, port, self.pull)
            else :                 
                banner = s.recv(1024)
                if banner.isempty():
                    s.sendall(b'WhoAreYou\r\n')
                    banner = s.recv(1024)
                    self.ports[port]["banner"] = banner.decode()
            
        except Exception:
            if not self.silent:
                print("No banner available")
            self.ports[port]["banner"] = "No banner available"
