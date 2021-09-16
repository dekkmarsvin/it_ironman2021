import requests
from configparser import ConfigParser

jsonheaders = {
    'Content-Type': 'application/json'
}

def sendreq(method="POST", url = None, headers=jsonheaders, data = None):
    try:
        response = requests.request(method=method, url=url, headers=headers, data=data, timeout=10)
        return response
    except Exception as err:
        print(err)