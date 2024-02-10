import concurrent
import ipaddress
import socket
import subprocess


class Target (): 
    
    def __init__(self, ip, port=65535):
        self.ip = ip
        self.hostname = ""
        self.status = False
        self.users = {}
        self.max_port = port
        self.ports = {}
        for port in range(1, self.max_port + 1):
            self.set_ports(port, False)
        
    def get_ip(self):
        return self.ip
    
    def set_ip(self, ip):
        self.ip = ip
    
    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status
    
    def get_ports(self):
        return self.ports
    
    def set_ports(self, port, state, service="", banner=""):
        self.ports[port] = {"state": state, "service": service, "banner": banner}
    
    def get_users(self):
        return self.users
    
    def set_users(self, user):
        self.users.append(user)
    
    def test_connection (self):
        if not ipaddress.ip_address(self.ip).is_global:
            try:
                target = socket.gethostbyname(str(self.ip))
                subprocess.check_output(["ping", "-c", "1", target])
                self.set_status(True)

            except Exception :
                self.set_status(False)
                
    def scanning(self, port, banner_mode, silent):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1) # need to be able to set it in the command line
        result = s.connect_ex((self.ip,port))
        
        if result == 0:
            self.set_ports(port, True)
            if banner_mode: 
                self.banner_grabbing(s, port)
        else:
            self.ports[port] = {"state": False, "service": "", "banner": ""}
        s.close()
    
    def scan_setup(self, banner_mode, silent, executor):
        self.test_connection()
        scan_host = [executor.submit(self.scanning, port, banner_mode, silent) for port in range(0, self.max_port, 1)]
        concurrent.futures.wait(scan_host)     
     

    def banner_grabbing(self, s, port):
        try:
            if port == 80:
                s.sendall(b"HEAD / HTTP/1.1\r\n\r\n")
                banner = s.recv(1024)
                
                self.ports[port]["banner"] = banner.decode()
            elif port == 21:
                banner = s.recv(1024)
                total_communication = banner + self.anonymous_ftp_login(s)
                self.ports[port]["banner"] = total_communication.decode()
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
            
    def anonymous_ftp_login(self, s):
        s.sendall(b"USER anonymous\r\n")
        user = s.recv(1024)
        s.sendall(b"PASS anonymous\r\n")
        password = s.recv(1024)
        return user + "\n" + password  