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