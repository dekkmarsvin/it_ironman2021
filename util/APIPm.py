import requests
from configparser import ConfigParser
import urllib.parse

jsonheaders = {
    'Content-Type': 'application/json'
}

xwwwformurlencodedheaders = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

def sendreq(method="POST", url = None, headers=jsonheaders, params={}, data = None):
    try:
        response = requests.request(method=method, url=url, headers=headers, params=params, data=data, timeout=10)
        return response
    except Exception as err:
        print(err)
