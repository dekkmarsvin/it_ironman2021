from sys import api_version
from types import SimpleNamespace
from configparser import ConfigParser
import json
from typing import Type
import hashlib
from base64 import b64decode, b64encode
from Cryptodome.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

from . import APIModel
from . import APIPm

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

def GetRespSign(msg:str, nonce:str, HashID:str):
    msg = json.loads(msg)
    SignStr = ""
    for parm in sorted(msg, key=lambda v: v.upper()):
        val = msg[parm]
        if(type(val) == dict or not val):continue
        SignStr = SignStr + f"{parm}={msg[parm]}&"
    SignStr = SignStr.removesuffix('&') + nonce + HashID
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
    return ct_bytes.hex().upper()

def AES_CBC_Decrypt(HashID, iv, data):
    try:
        key = str.encode(HashID)
        iv = str.encode(iv)
        data = bytes.fromhex(data)
        cipher = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
        pt = unpad(cipher.decrypt(data), AES.block_size)
        return pt.decode("utf-8")
    except (ValueError, KeyError):
        print("Incorrect decryption")

def Response_Decrypt(resp, HashID):
    js_resp = json.loads(resp.text)
    nonce = js_resp['Nonce']
    iv = GenIV(nonce)
    msg = js_resp['Message']
    msg = AES_CBC_Decrypt(HashID, iv=iv, data=msg)
    resp_vsign = js_resp['Sign']
    resp_csign = GetRespSign(msg=msg, nonce=nonce, HashID=HashID)
    return msg, resp_vsign == resp_csign

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

def OrderCreate(origin, cfg):
    #產生建立訂單交易(虛擬帳號、信用卡) - OrderCreate
    nonce = GetNonce(cfg)
    sign = GenSign(origin, nonce, cfg.HashID)
    iv = GenIV(nonce)
    msg = GenMessage(iv, origin, cfg.HashID)
    body = GenRequest(cfg=cfg, APIService="OrderCreate", sign=sign, nonce=nonce, message=msg)
    resp = APIPm.sendreq(url=cfg.Api_URL ,data=body)
    funbiz_msg = Response_Decrypt(resp, cfg.HashID)
    return funbiz_msg

def GenOrderQuery(cfg):
    #訂單交易查詢 - OrderQuery
    req = APIModel.ReqOrderQuery()

def GenOrderPayQuery(cfg):
    #訊息查詢服務 - OrderPayQuery
    print(cfg)

def GetNonce(cfg):
    payload = json.dumps({"ShopNo":cfg.ShopNo}, indent=4)
    resp = APIPm.sendreq(url=cfg.Nonce_URL, data=payload)
    return json.loads(resp.text)['Nonce']

def OrderPayQuery(ShopNo=os.environ['ShopNo'], PayToken=None):
    if(not ShopNo or not PayToken):return None
    payload = json.dumps({"ShopNo":ShopNo, "PayToken":PayToken}, indent=4)
    resp = APIPm.sendreq(url=cfg.Api_URL, data=payload)
    resp = json.loads(resp.text)
    print(resp)
    return resp

if __name__ == '__main__':
    # env = ConfigParser()
    # env.read('env.ini')
    # Hash = SimpleNamespace(A1 = env['App']['A1'], A2 = env['App']['A2'], B1 = env['App']['B1'], B2 = env['App']['B2'])
    # cfg = SimpleNamespace(Version = env['App']['Version'], ShopNo = env['App']['ShopNo'], HashID = HashID(Hash), \
    #     Api_URL = env['Server']['Api_URL'], Nonce_URL = env['Server']['Nonce_URL'])
    
    # org = APIModel.ReqOrderCreate(ShopNo=cfg.ShopNo, OrderNo="202007111119291751", Amount=60000, PayType="C", AutoBilling="Y", ExpMinutes=30, \
    #     PrdtName="信用卡訂單", ReturnURL="http://10.11.22.113:8803/QPay.ApiClient-Sandbox/Store/Return", BackendURL="https://sandbox.sinopac.com/funBIZ.ApiClient/AutoPush/PushSuccess")
    # print(GenOrderCreate(org, cfg))

    Hash = SimpleNamespace(A1 = os.environ['A1'], A2 = os.environ['A2'], B1 = os.environ['B1'], B2 = os.environ['B2'])
    cfg = SimpleNamespace(Version = os.environ ['Version'], ShopNo = os.environ['ShopNo'], HashID = HashID(Hash), \
                         Api_URL = os.environ['Api_URL'], Nonce_URL = os.environ['Nonce_URL'], BackendURL = os.environ['BackendURL'], \
                        ReturnURL = os.environ['ReturnURL'])

    neworder = APIModel.ReqOrderCreate(ShopNo="NA0249_001", OrderNo="2021100300001", Amount=40400, \
                PrdtName="IPhone 13 Pro Max 256g", ReturnURL=cfg.ReturnURL, \
                    BackendURL=cfg.BackendURL, PayType="C", AutoBilling="Y", PayTypeSub="ONE")
    msg, OK = OrderCreate(neworder, cfg)
    if(OK):print("建立訂單成功")
    else:print("建立訂單失敗")
    print(msg)

