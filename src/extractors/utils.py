thonimport requests

def fetch_data_from_url(url):
    """
    Fetch data from a URL.
    :param url: The URL to fetch data from
    :return: The HTTP response
    """
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from {url}")
    return response.text