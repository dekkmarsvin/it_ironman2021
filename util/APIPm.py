import requests

apiservice = "https://apisbx.sinopac.com/funBIZ/QPay.WebAPI/api/Order"
nonceservice = "https://apisbx.sinopac.com/funBIZ/QPay.WebAPI/api/Nonce"

jsonheaders = {
    'Content-Type': 'application/json'
}

def sendreq(method="POST", url = apiservice, headers=jsonheaders, data = None):
    try:
        response = requests.request(method=method, url=url, headers=headers, data=data)
        return response
    except Exception as err:
        print(err)