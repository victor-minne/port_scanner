from ftplib import FTP

def ftp_connect(ip, port, pull=False):
    """
    Connects to the FTP server.

    Parameters:
    - ip (str): The IP address of the FTP server.
    - port (int): The port of the FTP server.

    Returns:
    - socket: The socket object.
    """
    ftp = FTP(ip)
    try : 
        ftp.connect(ip, port)
    except ConnectionError:
        ftp.quit()
        raise ConnectionError("enable to connect to the FTP server")
    
    banner = ftp.getwelcome()
    anon_login = anonymous_ftp_login(ftp, pull)
    
    ftp.quit()
    return banner, anon_login 


def anonymous_ftp_login(ftp, pull):
    """
    Performs anonymous FTP login.

    Parameters:
    - s: The socket object.

    Returns:
    - str: The communication with the FTP server.
    """
    
    result = ftp.login(user="anonymous", passwd="")
    if result == "230 Login successful.":
        try :
            dir_list = ftp.retrlines('LIST')
            if pull:
                pull_files(ftp, pull)
        except ConnectionError:
            ftp.quit()
            raise ConnectionError("not able to list the directory")
        return result
    return "not able to login as anonymous" + result + "\n" + dir_list



def pull_files(ftp, pull):
    """
    Pulls files from the FTP server.

    Parameters:
    - s: The socket object.
    """
    try :
        files = ftp.nlst()
        for file in files:
            file_path = pull + file
            try : 
                with open(file_path, 'wb') as f:
                    ftp.retrbinary('RETR ' + file, f.write)
            except FileNotFoundError:
                ftp.quit()
                raise FileNotFoundError("not able to create the file, or retreive it from the FTP server")
    except ConnectionError:
        ftp.quit()
        raise ConnectionError("not able to pull the files")
    return "Files pulled successfully"
