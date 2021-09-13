from sys import api_version
from types import SimpleNamespace
from configparser import ConfigParser
import json
from typing import Type
import hashlib
from base64 import b64decode, b64encode
from Cryptodome.Cipher import AES
from Crypto.Util.Padding import pad, unpad

import APIModel

def xor_two_str(a,b):
    a = int(a,base=16)
    b = int(b,base=16)
    return hex(a ^ b)

def HashID(Hash:SimpleNamespace):
    str1 = (xor_two_str(Hash.A1, Hash.A2)[2:]).upper()
    str2 = (xor_two_str(Hash.B1, Hash.B2)[2:]).upper()
    # print(f"str1:{str1}, str2:{str2}")
    return str1 + str2 
    
def GenSign(origin, Nonce:str, HashID:str):
    SignStr = ""
    #不分大小寫排序變數
    for parm in sorted(origin.__dict__, key=lambda v: v.upper()):
        val = origin.__dict__[parm]
        # print(f"Parm:{parm}, Val:{val}, Types:{type(val)}")
        if(not type(val) == SimpleNamespace and origin.__dict__[parm] != None):
            if(type(val) == str and not val):continue
            SignStr = SignStr + f"{parm}={origin.__dict__[parm]}&"
    SignStr = SignStr.removesuffix('&') + Nonce + HashID
    sign = hashlib.sha256(SignStr.encode('utf-8')).hexdigest().upper()
    return sign

def GenIV(Nonce:str):
    return hashlib.sha256(Nonce.encode('utf-8')).hexdigest().upper()[-16:]

def AES_CBC_Encrpt(HashID, iv, data):
    key = str.encode(HashID)
    iv = str.encode(iv)
    data = str.encode(data)
    cipher = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    # return b64encode(ct_bytes).decode('utf-8')
    return ct_bytes.hex().upper()

def AES_CBC_Decrypt(HashID, iv, data):
    try:
        key = str.encode(HashID)
        iv = str.encode(iv)
        # data = b64decode(data)
        data = bytes.fromhex(data)
        cipher = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
        pt = unpad(cipher.decrypt(data), AES.block_size)
        return pt
    except (ValueError, KeyError):
        print("Incorrect decryption")

def SimNStoJson(sns:SimpleNamespace):
    for parm in sns.__dict__:
        val = sns.__dict__[parm]
        if(type(val) == SimpleNamespace):
            sns.__dict__[parm] = sns.__dict__[parm].__dict__
    js = json.dumps(sns.__dict__, indent=4, ensure_ascii=False)
    return js

def GenMessage(iv:str, origin:str, HashID:str):
    jstr = SimNStoJson(origin)
    ciphertext = AES_CBC_Encrpt(HashID, iv, jstr)
    return ciphertext

def GenRequest(cfg, APIService, sign, nonce, message):
    req = {'Version':cfg.Version, 'ShopNo':cfg.ShopNo, 'APIService':APIService, 'Sign':sign, 'Nonce': nonce, 'Message':message}
    js_req = json.dumps(req, indent=4, ensure_ascii=False)
    return js_req

def GenOrderCreate(origin, cfg):
    #產生建立訂單交易(虛擬帳號、信用卡) - OrderCreate
    nonce = GetNonce(cfg)
    sign = GenSign(origin, nonce, cfg.HashID)
    iv = GenIV(nonce)
    msg = GenMessage(iv, origin, cfg.HashID)
    body = GenRequest(cfg=cfg, APIService="OrderCreate", sign=sign, nonce=nonce, message=msg)
    print(body)
    print(f"iv:{iv}, key:{cfg.HashID}")

    import requests
    url = "https://apisbx.sinopac.com/funBIZ/QPay.WebAPI/api/"

    payload = body
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

def GenOrderQuery(cfg):
    #訂單交易查詢 - OrderQuery
    req = APIModel.ReqOrderQuery()

def GenOrderPayQuery(cfg):
    #訊息查詢服務 - OrderPayQuery
    print(cfg)

def GetNonce(cfg):
    import requests
    #POST https://apisbx.sinopac.com/funBIZ/QPay.WebAPI/api/Nonce with json content of body
    url = "https://apisbx.sinopac.com/funBIZ/QPay.WebAPI/api/Nonce"

    payload = json.dumps({"ShopNo":cfg.ShopNo}, indent=4)
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return json.loads(response.text)['Nonce']

if __name__ == '__main__':
    env = ConfigParser()
    env.read('env.ini')
    Hash = SimpleNamespace(A1 = env['App']['A1'], A2 = env['App']['A2'], B1 = env['App']['B1'], B2 = env['App']['B2'])
    cfg = SimpleNamespace(Version = env['App']['Version'], ShopNo = env['App']['ShopNo'], HashID = HashID(Hash))
    
    org = APIModel.ReqOrderCreate(ShopNo=cfg.ShopNo, OrderNo="201807111119291750", Amount=60000, PayType="C", AutoBilling="Y", ExpMinutes=30, \
        PrdtName="信用卡訂單", ReturnURL="http://10.11.22.113:8803/QPay.ApiClient-Sandbox/Store/Return", BackendURL="https://sandbox.sinopac.com/funBIZ.ApiClient/AutoPush/PushSuccess")
    GenOrderCreate(org, cfg)