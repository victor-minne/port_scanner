import requests

def get_robot_txt(ip):
    """
    Retrieves the robots.txt file from the specified IP address.

    Args:
        ip (str): The IP address to retrieve the robots.txt file from.

    Returns:
        requests.Response: The response object containing the robots.txt file.

    Raises:
        Exception: If there is an error retrieving the robots.txt file.
    """
    try:
        response = requests.get(ip + "/robots.txt")
        return response
    except Exception as e:
        raise e("Unable to get robots.txt file")

def get_sitemap_xml(ip):
    """
    Retrieves the sitemap.xml file from the specified IP address.

    Args:
        ip (str): The IP address to retrieve the sitemap.xml file from.

    Returns:
        requests.Response: The response object containing the sitemap.xml file.

    Raises:
        Exception: If there is an error retrieving the sitemap.xml file.
    """
    try:
        response = requests.get(ip + "/sitemap.xml")
        return response
    except Exception as e:
        raise e("Unable to get sitemap.xml file")
    
    
def get_techno_list():
    with open('res/techno.list', 'r') as file:
        lines = []
        for line in file:
            line = line.strip()
            lines.append(line)

    
def search_techno(header, r):
    result = []
    techno_list = get_techno_list()
    for param in header :
        if param.lower() in techno_list :
            result.append(param)
            
    for techno in techno_list :
        # change the r to get only the header.s
        if r.contains(techno):
            result.append(techno)
    # filter list to get unique items.
    return result 
    
    
def get_techno (ip, user_agent):
    
    try :
        header_user_agent = {'user-agent': user_agent}
        header = requests.head(ip, headers=header_user_agent)
        r = requests.get(ip, headers=header_user_agent)
        techno_list = search_techno(header, r)
    except ConnectionError :
        raise ConnectionError("something went wrong while getting technos")
    return techno_list
    