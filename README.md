# IT鐵人賽2021

- [IT鐵人賽2021](#it鐵人賽2021)
  - [[Day1] 金融支付API](#day1-金融支付api)
    - [要做什麼:建置接入金融支付API的應用](#要做什麼建置接入金融支付api的應用)
    - [會用什麼:應用場景](#會用什麼應用場景)
  - [[day2] 付款流程 & 取得(Nonce)](#day2-付款流程--取得nonce)
    - [資料準備](#資料準備)
    - [付款系統](#付款系統)
  - [[Day3] 安全簽章 - XOR加密(HashID)](#day3-安全簽章---xor加密hashid)
    - [API流程](#api流程)
    - [產生HashID](#產生hashid)
  - [[day4] 安全簽章 - 產生訂單 & 簽章](#day4-安全簽章---產生訂單--簽章)
    - [準備訊息文本](#準備訊息文本)
    - [計算簽章Sign](#計算簽章sign)
  - [[day5] Python發送Request接收Response與永豐API串接參數](#day5-python發送request接收response與永豐api串接參數)
    - [Python實作 Request發送](#python實作-request發送)
    - [永豐API參數](#永豐api參數)
  - [[day6] AES-CBC 內文加密機制(Message)](#day6-aes-cbc-內文加密機制message)
    - [實作計算IV](#實作計算iv)
    - [AES CBC 計算實作](#aes-cbc-計算實作)
    - [Python實作計算AES CBC](#python實作計算aes-cbc)
  - [[day7] API回覆內容(Response)解析 & 驗證(sign)](#day7-api回覆內容response解析--驗證sign)
    - [訊息文本AES CBC 解密](#訊息文本aes-cbc-解密)
    - [以Python實作解密Message](#以python實作解密message)
    - [驗算Respnse中Sign](#驗算respnse中sign)
    - [以Python實作驗算Response Sign](#以python實作驗算response-sign)
  - [[day8] 實務搭建 - 儲值卡，系統概述](#day8-實務搭建---儲值卡系統概述)
    - [會員卡功能 - 需求分析](#會員卡功能---需求分析)
    - [資料庫結構](#資料庫結構)
    - [前端實作](#前端實作)
    - [後端實作](#後端實作)
  - [[day9] 建置SQL DB](#day9-建置sql-db)
    - [初始化資料庫](#初始化資料庫)
    - [使用Python調用sqlite3](#使用python調用sqlite3)
      - [載入資料庫](#載入資料庫)
      - [初始化資料庫(執行SQL檔案)](#初始化資料庫執行sql檔案)
      - [新增一個測試帳號(插入資料至指定Table)](#新增一個測試帳號插入資料至指定table)
      - [查詢User資料(SELECT from Table)](#查詢user資料select-from-table)
  - [[day10] Flask Python API Service](#day10-flask-python-api-service)
    - [設定測試API](#設定測試api)
  - [day[11] Hello Line - 第一個Line訊息](#day11-hello-line---第一個line訊息)
    - [產生 Assertion Signing Key(KID)](#產生-assertion-signing-keykid)
    - [實作取得JWT](#實作取得jwt)
    - [實作取得channel_access_token](#實作取得channel_access_token)
    - [Hello Line，發送訊息](#hello-line發送訊息)
  - [[day12]Heroku 基本使用](#day12heroku-基本使用)
    - [套件安裝](#套件安裝)
    - [下載並啟用範例專案](#下載並啟用範例專案)
    - [建立第一個Heroku App](#建立第一個heroku-app)
    - [Procfile](#procfile)
    - [requirements環境套件](#requirements環境套件)
    - [本機運行測試](#本機運行測試)
    - [將修改完成的新版本上傳到雲端](#將修改完成的新版本上傳到雲端)
    - [設定環境變數](#設定環境變數)
    - [其他功能](#其他功能)
  - [[day13] 設定gunicorn Logging](#day13-設定gunicorn-logging)
    - [gunicorn log 使用方式](#gunicorn-log-使用方式)
    - [使用Heroku 模組以從網頁瀏覽logs](#使用heroku-模組以從網頁瀏覽logs)
  - [[day14] 接收使用者的Line訊息](#day14-接收使用者的line訊息)
    - [實作並部署回聲機器人](#實作並部署回聲機器人)
      - [加機器人為好友](#加機器人為好友)
    - [過程解析](#過程解析)
  - [[day15]幾個常用的LineAPI](#day15幾個常用的lineapi)
    - [取得機器人資訊](#取得機器人資訊)
    - [推送、回覆訊息](#推送回覆訊息)
    - [取得使用者資訊](#取得使用者資訊)
    - [取得使用者訊息中的非文字內容](#取得使用者訊息中的非文字內容)
    - [Line-SDK的意外處理](#line-sdk的意外處理)
  - [[day16]機器人對話紀錄](#day16機器人對話紀錄)
    - [Postgres 初始化 & 連線](#postgres-初始化--連線)
      - [新增Postgres模組到你的專案](#新增postgres模組到你的專案)
      - [建立表格](#建立表格)
      - [連線](#連線)
    - [紀錄Line對話](#紀錄line對話)
    - [Summary](#summary)
  - [[day17]使用者名稱表格](#day17使用者名稱表格)
    - [實作紀錄使用者資訊](#實作紀錄使用者資訊)
      - [Postgresql採到的坑](#postgresql採到的坑)
  - [[day18] 追蹤 & 封鎖事件處理](#day18-追蹤--封鎖事件處理)

## [Day1] 金融支付API

大大大優惠，XX行動支付，現在推出認同卡，78910%大大大回饋.....

隨著手機成為現代人的一部份，功能隨著科技與創意發想而繁多，現在，金融App開發者們想要取代的是-**現金**，現今其實沒什麼不好用，缺點就是現金就只是現金，作為付款方式，最為及時，但也較難以創造邊際價值，也有一些實體上的風險，啊扯遠了，對於開發者來說，接入行動支付的最主要目的就是建置一個方便的消費者付款方式，支付速度更為快捷，數位化統計，不論實體或雲端均可交易

### 要做什麼:建置接入金融支付API的應用

相較於傳統的App開發，較少碰到與金錢相關的系統應用，而一旦與$$有關，各項法規與身分驗證便是開發者需要仔細處理反覆驗證的部分，畢竟出錯了可是**麻煩麻煩**，在掃碼付款，手機綁定信用卡支付等的應用後都有複雜的身分驗證、加密資訊交換，而實作這些內容便是本次鐵人賽的主題

### 會用什麼:應用場景

首先，實作接入銀行API，處理對接的所需資料，再來準備前後端系統，基本上會用Python撰寫前後端系統，再來看看實際用途所需

- todo list
  - [] 加密
  - [] 參數處理
  - [] 對接系統
  - [] 訂單
  - [] 後端系統
  - [] 前端系統

大概醬

## [day2] 付款流程 & 取得(Nonce)

### 資料準備

啊以為第二天開始就是程式碼喔，NONONO，要接入金融機構的系統，不是任何人都能直接跑進去Say Hi誰付錢給我所以給我錢錢，得準備一大堆表格跟付款取得憑證還有1234567等等步驟，啊不過幸好這次沒有真的要收錢，所以只要連上**免費**的測試環境，就可以試用金融API了

本回採用永豐銀行的消費支付API進行開發，你會需要申請一個【商店代號】，以及取得【認證金鑰】以接入系統，這兩項資訊可以在[這邊](https://developer.sinopac.com/ithome)取得，以下表格內數值為範例

功能|數值
---|---
商店代號|NA0001_001
A1|86D50DEF3EB7400E
A2|01FD27C09E5549E5
B1|9E004965F4244953
B2|7FB3385F414E4F91

### 付款系統

消費支付方式，分為數種，不論是使用虛擬帳號匯款，或是信用卡、掃碼支付均為以下流程構成

消費者購買-->商家系統建立訂單-->金流系統回傳付款方式-->商家系統顯示付款指示給消費者-->消費者付款給金流系統-->金流系統通知商家

而其中的技術構成，其實就是商家系統與金流系統間通過API的交互溝通，看到這邊，請先安裝[Postman](https://www.postman.com/)準備測試API連通，當然也可以用自己習慣的方式，只要能收發HTTPS(TLS1.2)的UTF-8編碼json就行

永豐的金融API依據「電子銀行業務安全控管作業基準」，制定安全簽章(Sign)與內文加密機制(Message)

不可否認性，是電子支付的重要實現功能，為了確保付款資訊不被偽造竄改，各家系統都有各自的簽章與驗證方式，而在永豐的消費支付，其中一項保護就是nonce，此一隨機值用於確保API通訊的時效性與來源一致(IP驗證)

請在Postman中使用**POST**方式，向<https://apisbx.sinopac.com/funBIZ/QPay.WebAPI/api/Nonce>傳送Request以取得Nonce吧

```json
// Body
{
 "ShopNo"://你的商店代碼e.g., NA0001_001
}
```

正確執行後，永豐系統會回傳一組Json格式的Nonce參數

```json
{
"Nonce":"NjM2NjI2NjM2ODIxOTcuNDo3MGY3YjY1YTQ3Y2ViOGUyNzA4YTY5Yzc3ODVjY2NjNTkwMGU4YzI4YTY4ZWI5NDg4MTdhOTE5NjY3YjhkODA0"
}
```

恭喜你已經踏出了與銀行系統串接的第一步，下一篇開始將說明這個參數能幹嘛，可惜不可以吃

## [Day3] 安全簽章 - XOR加密(HashID)

### API流程

I have A Nonce, I have A key, Uh It's time to Crypto.

為確保資料安全性，**每次**呼叫API都必須取得**Nonce**後計算出安全簽章及訊息加密，概述基本流程如下:

商家|通訊方向|永豐金流系統
---|---|---
要求取得Nonce|-->
||<--|回覆Nonce
產生API內容||
要求API服務|-->|
||<--|回覆要求資料

前一天的文章結尾，包含一個取得Nonce的API Request，現在將利用該API結合金鑰資訊產生安全簽章(Sign)

### 產生HashID

由四組Hash金鑰進行兩兩XOR位元運算，再相加的32位元字串，後續用作AES加密的Key使用

ValA|ValB|XOR
---|---|---
0|0|0
0|1|1
1|0|1
1|1|0

計算流程參考**XOR運算**

1. A1：4D9709D699CA40EE
2. A2：5A4FEF83140C4E9E
3. B1：BC74301945134CB4
4. B2：961F67F8FCA44AB9
5. 字串１(A1 XOR A2)：17d8e6558dc60e70
6. 字串２(B1 XOR B2)：2a6b57e1b9b7060d
7. Hash ID(字串 1+字串 2 後英文轉大寫)：17D8E6558DC60E702A6B57E1B9B7060D

以Python實現

```python
def xor_two_str(a,b):
    a = int(a,base=16)
    b = int(b,base=16)
    return hex(a ^ b)

def HashID(Hash:SimpleNamespace):
    str1 = (xor_two_str(Hash.A1, Hash.A2)[2:]).upper()
    str2 = (xor_two_str(Hash.B1, Hash.B2)[2:]).upper()
    print(f"str1:{str1}, str2:{str2}")
    return str1 + str2 
```

產生出來的HashID必須搭配其他參數一起使用，在此必須先撰寫一個產生API服務規格的程式，以JSON格式的API Request，可以自行撰寫，或參考我的寫法

```json
{
  //API服務規格範例
 "ShopNo": "BA0026_001",
 "OrderNo": "A201804270001",
 "Amount": 50000,
 "CurrencyID": "TWD",
 "PayType": "A",
 "ATMParam": { "ExpireDate": "20180502" },
 "CardParam": { },
"ConvStoreParam": { },
 "PrdtName": "虛擬帳號訂單",
 "ReturnURL": "http://10.11.22.113:8803/QPay.ApiClient/Store/Return",
 "BackendURL": "http://10.11.22.113:8803/QPay.ApiClient/AutoPush/PushSuccess"
}
```

以Python實現產生API服務規格的資料結構(建立訂單)

```python
def ReqOrderCreate(ShopNo = "", OrderNo = "", Amount = 0, CurrencyID = "TWD", PrdtName = "", Memo = "", \
    Param1 = "", Param2 = "", Param3 = "", ReturnURL = "", BackendURL = "", PayType = "", ExpireDate = "", \
    AutoBilling = "Y", ExpBillingDays = 7, ExpMinutes = 10, PayTypeSub = "ONE"):
    # 永豐銀行- 數位金流 API 技術規格文件 page 32
    return SimpleNamespace(ShopNo = ShopNo, OrderNo = OrderNo, Amount = Amount, CurrencyID = CurrencyID, PrdtName = PrdtName, Memo = Memo, \
    Param1 = Param1, Param2 = Param2, Param3 = Param3, ReturnURL = ReturnURL, BackendURL = BackendURL, PayType = PayType, \
    ATMParam = SimpleNamespace(ExpireDate = ExpireDate), CardParam = SimpleNamespace(AutoBilling = AutoBilling, \
    ExpBillingDays = ExpBillingDays, ExpMinutes = ExpMinutes, PayTypeSub = PayTypeSub))
```

## [day4] 安全簽章 - 產生訂單 & 簽章

### 準備訊息文本

依照參數說明，建立訂單的資料結構[(DAY3-參考)]("https://ithelp.ithome.com.tw/articles/10263834")，詳細參數規格可以在永豐API技術規格文件內找到，此處先以訂單建立(OrderCreate)API進行測試，訂單細節如下:

- 商店代號:NA0249_001
- 訂單編號:2021091500001
- 金額:40400
- 收款名稱:IPhone 13 Pro Max 256g
- 付款完成頁面:<https://0.0.0.0/store/Return>
- 主機端:<https://0.0.0.0/bakcend>
- 付款方式:信用卡
  - 使用自動請款
  - 一次付清

故使用的參數為:

- ShopNo=NA0249_001
- OrderNo=2021091500001
- Amount=40400
- PrdtName=IPhone 13 Pro Max 256g
- ReturnURL="https://0.0.0.0/store/Return"
- BackendURL="https://0.0.0.0/bakcend"
- PayType=C
  - AutoBilling=Y
  - PayTypeSub=ONE

以Python實作:

```python
neworder = APIModel.ReqOrderCreate(ShopNo="NA0249_001", OrderNo="2021091500001", Amount=40400, \
            PrdtName="IPhone 13 Pro Max 256g", ReturnURL="https://0.0.0.0/store/Return", \
                BackendURL="https://0.0.0.0/bakcend", PayType="C", AutoBilling="Y", PayTypeSub="ONE")
```

這邊吐槽一下信用卡API測試環境只能測試**一次付清**，否則會跳**E0602 - 收款方式未啟用**錯誤，另外還有**預計自動請款天數**，在設定自動請款時按照說明書應該會忽略，結果會跳日期範圍不正確錯誤，請款日期範圍也不是文件上的1-21天，而是1-7天

### 計算簽章Sign

在取得Nonce、HashID、訊息文本等三個參數後，才能夠進行安全簽章(Sign)計算，計算方式概述:

1. 移除訊息文本中空的參數與節點參數(如留空的參數與ATMParam與CardParam)
2. 將參數以**不分大小寫**方式遞增排序
3. 以[參數名稱1]=[數值1]&[參數名稱2]=[數值2].....的方式串接參數組成字串
4. 加上Nonce與HashID
5. 進行字串SHA256計算

以上節iPhone的信用卡訂單為範例，產生的訊息文本為:

```json
{
    "ShopNo": "NA0249_001",
    "OrderNo": "2021091500002",
    "Amount": 40400,
    "CurrencyID": "TWD",
    "PrdtName": "IPhone 13 Pro Max 256g",
    "Memo": "",
    "Param1": "",
    "Param2": "",
    "Param3": "",
    "ReturnURL": "https://0.0.0.0/store/Return",
    "BackendURL": "https://0.0.0.0/bakcend",
    "PayType": "C",
    "ATMParam": {
        "ExpireDate": ""
    },
    "CardParam": {
        "AutoBilling": "Y",
        "ExpBillingDays": 7,
        "ExpMinutes": 10,
        "PayTypeSub": "ONE"
    }
}
```

進行步驟1.移除訊息文本中空的參數與節點參數(如留空的參數與ATMParam與CardParam):

```json
{
    "ShopNo": "NA0249_001",
    "OrderNo": "2021091500002",
    "Amount": 40400,
    "CurrencyID": "TWD",
    "PrdtName": "IPhone 13 Pro Max 256g",
    "ReturnURL": "https://0.0.0.0/store/Return",
    "BackendURL": "https://0.0.0.0/bakcend",
    "PayType": "C",
}
```

進行步驟2.將參數以**不分大小寫**方式遞增排序、3. 以[參數名稱1]=[數值1]&[參數名稱2]=[數值2].....的方式串接參數組成字串，記得去掉末尾的'&'

```python
order = "Amount=40400&BackendURL=https://0.0.0.0/bakcend&CurrencyID=TWD&OrderNo=2021091500002&PayType=C&PrdtName=IPhone 13 Pro Max 256g&ReturnURL=https://0.0.0.0/store/Return&ShopNo=NA0249_001"
```

進行步驟4. 加上Nonce與HashID

```python
nonce = "NjM3NjczMjQwNzM1NTAuOTo5ZWE1MmFhYzk0NDgwMzljY2RiNjhjOGU0MGU3ODc0NzFiMTIwNmNkMTViZWU4MzUwZDU3Zjg1M2VhNjIwODRj"
HashID = "17D8E6558DC60E702A6B57E1B9B7060D"

str_before_sign = "Amount=40400&BackendURL=https://0.0.0.0/bakcend&CurrencyID=TWD&OrderNo=2021091500002&PayType=C&PrdtName=IPhone 13 Pro Max 256g&ReturnURL=https://0.0.0.0/store/Return&ShopNo=NA0249_001NjM3NjczMjQwNzM1NTAuOTo5ZWE1MmFhYzk0NDgwMzljY2RiNjhjOGU0MGU3ODc0NzFiMTIwNmNkMTViZWU4MzUwZDU3Zjg1M2VhNjIwODRj17D8E6558DC60E702A6B57E1B9B7060D"
```

進行步驟5. 進行字串SHA256計算

```python
sign = "3c883d53f7732ec7c3f8c9d0232691545855b60507b199094a4cde71c911f522"
```

以下為Python完整實作:

```python
'''
Sample Env.ini
[App]
Version = 1.0.0
ShopNo = BA0026_001
A1 = 86D50DEF3EB7400E
A2 = 01FD27C09E5549E5
B1 = 9E004965F4244953
B2 = 7FB3385F414E4F91

[Server]
Api_URL = https://apisbx.sinopac.com/funBIZ/QPay.WebAPI/api/Order
Nonce_URL = https://apisbx.sinopac.com/funBIZ/QPay.WebAPI/api/Nonce
'''
def main():
  env = ConfigParser()
  env.read('env.ini')
  Hash = SimpleNamespace(A1 = env['App']['A1'], A2 = env['App']['A2'], B1 = env['App']['B1'], B2 = env['App']['B2'])
  cfg = SimpleNamespace(Version = env['App']['Version'], ShopNo = env['App']['ShopNo'], HashID = HashID(Hash))
  neworder = APIModel.ReqOrderCreate(ShopNo="NA0249_001", OrderNo="2021091500002", Amount=40400, \
                  PrdtName="IPhone 13 Pro Max 256g", ReturnURL="https://0.0.0.0/store/Return", \
                      BackendURL="https://0.0.0.0/bakcend", PayType="C", AutoBilling="Y", PayTypeSub="ONE")
  OrderCreate(neworder, cfg)

def OrderCreate(origin, cfg):
  nonce = GetNonce(cfg)
  sign = GenSign(origin, nonce, cfg.HashID)

def GetNonce(cfg):
  payload = json.dumps({"ShopNo":cfg.ShopNo}, indent=4)
  resp = APIPm.sendreq(url=APIPm.nonceservice, data=payload)
  return json.loads(resp.text)['Nonce']

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
```

如何產生簽章大家都會了嗎；阿好像忘了寫怎麼在Python內丟Request，明天補寫，斯米麻賽

## [day5] Python發送Request接收Response與永豐API串接參數

### Python實作 Request發送

如果你的Python環境沒有requests模組

```cmd
pip install requests
```

向網站/網路資源請求資料(request)，主要有GET/POST兩種方式，如果溝通正常，通常會獲得回應response，除了資料外還會有一個http status code，關於網路HTTP具體技術細節這邊不會講解，有興趣可以自行Google

個人建議會重複使用的常數都集中寫在設定檔案中，再用ConfigParser讀取，這樣可以統一修改整份專案的常數

```ini
[Server]
#永豐消費支付API服務網址
Api_URL = https://apisbx.sinopac.com/funBIZ/QPay.WebAPI/api/Order
#永豐消費支付API-Nonce服務網址
Nonce_URL = https://apisbx.sinopac.com/funBIZ/QPay.WebAPI/api/Nonce
```

API以Json格式溝通，建立一個基本的Json Headers

```python
jsonheaders = {
    'Content-Type': 'application/json'
}
```

實作發送request

```python
#讀取設定檔
env = ConfigParser()
env.read('env.ini')
cfg = SimpleNamespace(Api_URL = env['Server']['Api_URL'], Nonce_URL = env['Server']['Nonce_URL'])

#發送POST的request
def sendreq(method="POST", url = None, headers=jsonheaders, data = None):
  try:
    response = requests.request(method=method, url=url, headers=headers, data=data)
    return response
  except Exception as err:
    print(err)
```

產生JSON格式的Request實作

```python
def GenRequest(cfg, APIService, sign, nonce, message):
  req = {'Version':cfg.Version, 'ShopNo':cfg.ShopNo, 'APIService':APIService, 'Sign':sign, 'Nonce': nonce, 'Message':message}
  #ensure_ascii=False，關閉中文ascii轉換
  js_req = json.dumps(req, indent=4, ensure_ascii=False)
  return js_req
```

返回的Response中的參數定義可以參考[w3schools](https://www.w3schools.com/python/ref_requests_response.asp)，實際會使用到的只有statud_code與content

```python
#判斷是否Ok
response.OK
# TRUE/FALSE

#將content轉成str
response.text

#將content轉成json
response.json()
```

### 永豐API參數

- 由永豐銀行指定的參數
  - Version(API版本，現固定為1.0.0)
  - ShopNo
  - Nonce
- 由店家自行產生
  - APIService(e.g. OrderCreate、OrderQuery、OrderPayQuery.....)
  - Sign(SHA256)
    - JSON
    - Nonce
    - HashID
  - Message(AES CBC)
    - JSON
    - HashID
    - IV

說明請見數位金流 API 技術規格文件p.13，以下為完成簽章與內文加密的完整Request

```json
{
  "Version": "1.0.0",
  "ShopNo": "NA0001_001",
  "APIService": "OrderCreate",
  "Sign": "7788EE61DD450944992641B3B2F8210B81A0AE97908BC19825F2A82C0F72EA43",
  "Nonce": "NjM2NjY5MDQ3OTQwMzIuMTphZmJjODBhOTM5NzQ1NjMyNDFhZTczMjVjYzg0Mjg5ZjQxYTk2MWI2ZjNkYTA0NDdmOTRhZjU3ZTIzOWJlNDgz",
  "Message": "4FE341D3A8C30C9A50573F3008F7B1CA8DD96FB2A4346D83936E5C4FDB21E87BA9E3D36A6635C6F5EBBD5438F3CA8FE97DEBB2ADBC82F92BF3C840B3128D8F00116536E7C936D7D587F6220C52C1367DF2BE9CBB16C6A7C6242AA8B38CD2E576328CF727E50FFA49B4F9FBE5DF10986C5299F9FC26E23E956AFDFB92B731FDA84ABEF1C89E0CD0A8CA8F7C23DC2D06E12A6F916EC47CDD9B4D4F87AC0B687EE1088A19F2C35C0FD8B0C97745B926FBAA48FEEDEB826C2C22743DB46781FF220ECA409FC150908540271E60184729C08C73275C54125C3F814FF33CA79A0E1B3902D446925FCC8235809FCBAB7E372D8C29E424CEFF0AD1CBD41E843714EB365158F2FC0B2E6FB48176D5CFF6B68F4BED4D7484C1A4723ABD059DA64A6703B30B0199B170FDF059899552FA1818ABA5B0D0E21014513985A738D59851EDF0B1CFB36A7B7B727109BE7789D284C75E5D694DFC9B7060DCBFD8C7915C95C4E0F29B"
}
```

最後一個Message參數怎麼看不懂，安啦明天將說明如何進行內文的ABS CBC加密

## [day6] AES-CBC 內文加密機制(Message)

訊息文本使用AES-CBC模式加密傳送，接收的結果亦以相同規則加密

必要的參數|如何取得
---|---
JSON訊息文本|[Day3](https://ithelp.ithome.com.tw/articles/10263834)
HashID|[Day3](https://ithelp.ithome.com.tw/articles/10263834)
IV|[Nonce](https://ithelp.ithome.com.tw/articles/10263682)做SHA256後轉大寫後16碼

### 實作計算IV

假設本次取得的Nonce為:NjM3NjczODg3Mjc5MTYuNjo1ZDI5ZTQ3YjBlNzY2NTc4ODI3YzM0ZjdiMjlmYjg0MWQ3Y2NlYzI5NmM0NjI2MzA3NWRkYTNlNzQ1NzdhMWY4

字串進行sha256後:54164b54f6f9366b8377dd69b43e9970b0c95dee26be66402d3e2ea879b80c63

IV為字串尾端16碼的英文大寫:2D3E2EA879B80C63

Python實作如下

```python
def GenIV(Nonce:str):
  return hashlib.sha256(Nonce.encode('utf-8')).hexdigest().upper()[-16:]
```

### AES CBC 計算實作

如果對密碼學有興趣，可以自己Google，這邊直接用先前iphone的訂單進行實作

```json
{
    "ShopNo": "NA0249_001",
    "OrderNo": "2021091500002",
    "Amount": 40400,
    "CurrencyID": "TWD",
    "PrdtName": "IPhone 13 Pro Max 256g",
    "Memo": "",
    "Param1": "",
    "Param2": "",
    "Param3": "",
    "ReturnURL": "https://0.0.0.0/store/Return",
    "BackendURL": "https://0.0.0.0/bakcend",
    "PayType": "C",
    "ATMParam": {
        "ExpireDate": ""
    },
    "CardParam": {
        "AutoBilling": "Y",
        "ExpBillingDays": 7,
        "ExpMinutes": 10,
        "PayTypeSub": "ONE"
    }
}
```

假設這次取得的nonce為:NjM3Njc0MDQxODY5OTYuNDowNDIxNTg3ODM5MDFhNTU1ZjYwYzMzMzg0NDEyMzUxNmQ5OTBlZWU1NDY2NjY2NDkyZjE5YTc3OTE2ZDExNjNh

計算出IV:3C7B67201DC59932

假設金鑰為:

- A1 = 86D50DEF3EB7400E
- A2 = 01FD27C09E5549E5
- B1 = 9E004965F4244953
- B2 = 7FB3385F414E4F91

HashID為:87282A2FA0E209EBE1B3713AB56A06C2

將訊息文本以AES-CBC模式加密，Key Size=256，AESKEY=HashID，IV，以16進制HEX模式輸出的結果:

16D2F25D277F33FC46D1B8B8D693416F159CE3E8E62B829EB0D6E3D0863B50F07D6C2240EC73EE47459C8E06992D6F59B50831B52A80429A86AB01FF6149E12500162C68DE232D3777E097FE4F58BEDC238B0105D3826E8CC3A69CDF946B5513517AD89E9C966DD41A82A3FF6CAA22DCB8FCAD28614444CE5272D121792083D6F9401DAF6890792C46D7A918785280224A04FD25E58421021141F5C21FCA4341328887657D20AD82CA99D2F42761F9BAC6911AF835799356A8A4647CD097DCEA88D7DD3DA57CACCA572711D7C248B10894F7E62A3B1A675F1EFDF9B4FB3B3C7F110F9F27875E6F44647F54881E6FCF1CB3709C38462D2B52BCC871CA88EFA86EF4D890615C107528C4AA90CF79B87FF3569ED3F7C5B47837E2706E11A381B5219F904D5CF01B8D32B4FB994544924CE5A37F520B12B759E734596CA0472066341444DB811138F96F16E8A6E50370D8032C777C23C1700DF8784B1B68562827CA6765BE64C1F5F8F7BE9205FC35F1D998DE6715407CC0AE48434738B016FCF497E3DB001C158F5C639A2A40F429BA56E6B6587433B851DBEF723218CE6315F67DA19D0EAF121745F867F8A6EC174B37CC799534C2422354C326A2D4D3E64BDBA164D053FD6B02557A34291C3B364C2003E38724DF077E41627D0D90684138D7A42C418C026BD1292A4976327989E13BDEFCF3643E2E7136594ADC5FE5612EA3B1042C1593AB3CF6A32354E5E066FF3DF3

可以使用[devglan](https://www.devglan.com/online-tools/aes-encryption-decryption)進行加解密驗證測試

### Python實作計算AES CBC

參考[此篇](https://pycryptodome.readthedocs.io/en/latest/src/installation.html)進行PyCryptodome套件安裝

```python
from Cryptodome.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def AES_CBC_Encrpt(HashID, iv, data):
  key = str.encode(HashID)
  iv = str.encode(iv)
  data = str.encode(data)
  cipher = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
  ct_bytes = cipher.encrypt(pad(data, AES.block_size))
  return ct_bytes.hex().upper()

ciphertext = AES_CBC_Encrpt(HashID, iv, origin_Message)
```

現在已經湊齊發送API的所有參數(ShopNo、APIServer、Sign、Nonce、Message)了，明天將正式的將訂單資訊傳送到永豐的API伺服器，並測試功能

## [day7] API回覆內容(Response)解析 & 驗證(sign)

### 訊息文本AES CBC 解密

將昨天產生產生的訊息文本，傳送至測試伺服器<https://apisbx.sinopac.com/funBIZ/QPay.WebAPI/api/Order>，如果沒有問題的話會收到如下訊息:

```json
{
  "Version": "1.0.0",
  "ShopNo": "NA0249_001",
  "APIService": "OrderCreate",
  "Sign": "FBF41F9BFA5607F5141D508DA6B914DCAB97CE7CDE22EE636C9FDD81A9AC3277",
  "Nonce": "NjM3Njc0NzY1MDExMjc6MjVmMDE2NDUyYThjNDE4ODY1MmI4Mzk0OGM3YWY1Mjg0M2Y4NDdlMjAyMTk0YWM3MGFhZGZmNDcyMGQ5ZjhjNw==",
  "Message": "FAE9E297DB4D0B16D3E5A56561B28DDC41CD135B23D5309F971091033425405BA96669FE5A27B1D42DC4EB9636EBB0D9D9D618BC2B3969124A4F73CBB760CB83084623E1C2DED846BB46525E1B74F187EEF42A0F483AC49B0A12268D28452F44D268D38BDB91C464B74B1BB80D6DFC372622D8006005B0ABF5637287CB587FCE6ABB9D2BA377A29EC2E7E696CFDE2E305739CF2E6CBC1F2B71741064CA21CE3A6C6BFBAD663140A4CCC5AB24BE77569A26E1EA3A71EC2BC7AFC6E0F43ED537E42CDF535E910E25413BF4BC649D800F592FEA277BA18BF312EDD9A062D7F24A6405AC01EEF3F7F55EBC5978EEFC7AB097A802A1D05B675CC08E5ABD3FD9106EE0C624839EB0451EBE0F10E85C6DFCE4C9E0D29B3E633928F1A73102C04FA9DB91D7391D8917DC263437DBC50A7ACAF2CA06F8114669F783EF5189925B61EC9D7ECC3C504D09996665BC7CD3C3725F5D778F1D843FC42183153E565BF06307405F30401BA7E83EFAC91B54612D92E284F3BCFE324E26F8E7BFB1AE6326D96E2513D53A4D25DC1C1C24437A403A5BF281DA95A4EE018D6224F18128EB5FBFF3EF73EEE19E0EFD9429AB2976AB70C8DB050EFD81DB591831FD820157ACC4B60F101ABEF75AAA420EFF4C6FD7495226872B410CB87E958E7C92BFF3E3D35B4367B927F167A30F495876E82428ACC0D51BD61C7D30DB0A5FAEA26CDA24F79EA132000FFCF9C2E6EBCA124C6D8F546DF954C333"
}
```

通過先前產生訊息文本的相同方式進行解密(但本回Nonce由回應中的欄位取得)，分別得出

- Nonce:NjM3Njc0NzY1MDExMjc6MjVmMDE2NDUyYThjNDE4ODY1MmI4Mzk0OGM3YWY1Mjg0M2Y4NDdlMjAyMTk0YWM3MGFhZGZmNDcyMGQ5ZjhjNw==
- AESKey(HashID):87282A2FA0E209EBE1B3713AB56A06C2
- IV:15FE64E9D28D8934

將Message欄位取出，以**Hex**方式讀取，同樣用AES-CBC(256bits)方式進行解密，會得出

```json
{"OrderNo":"2021091500002","ShopNo":"NA0249_001","TSNo":"NA024900000173","Amount":40400,"Status":"S","Description":"S0000 – 處理成功","Param1":"","Param2":"","Param3":"","PayType":"C","CardParam":{"CardPayURL":"https://sandbox.sinopac.com/QPay.WebPaySite/Bridge/PayCard?TD=NA024900000173&TK=a135ccb2-2e4c-4af4-b4ef-dfece6367731"}}
```

### 以Python實作解密Message

```python
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

undecrypt_msg = js_resp['Message']
msg = AES_CBC_Decrypt(HashID, iv=iv, data=undecrypt_msg)
```

### 驗算Respnse中Sign

看到這邊，你一定想哇成功了對不對，其實還沒有，還少了最後一步，簽名驗證(Sign)，收發的資訊傳輸過程都需要驗證訊息文本與金鑰的配對，以確認資料的防竄改，關於如何產生Sign，可以[參照Day4](https://ithelp.ithome.com.tw/articles/10264251)，在這邊我們要取訊息文本中的Sign，與解密後Message中的參數進行比對是否相同

### 以Python實作驗算Response Sign

```python
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

resp_vsign = js_resp['Sign']
resp_csign = GetRespSign(msg=msg, nonce=nonce, HashID=HashID)

if(resp_vsign == resp_csign):
  print("簽章檢驗成功")
  return true
else:
  print("簽章驗證失敗")
  return false
```

呼，到現在已經將大致上的API如何使用完成時做了，接下來準備小跑進入實作環節，搭建一個儲值卡系統~~希望有時間做得完~~

## [day8] 實務搭建 - 儲值卡，系統概述

將錢先放到你的金卡，可以享大大大優惠，點點卡、OO卡、XX卡、網咖等都是先儲值再消費，這邊將實作一個基本的儲值卡系統，並將儲值的金流部分串接永豐API

在打開手機上的點點卡App後，可以大致整理出，一個會員卡系統，具有下列功能:

1. 儲值
   1. 信用卡儲值
   2. ATM儲值
   3. 臨櫃儲值
2. 消費
   1. 商品瀏覽
   2. 訂單系統

### 會員卡功能 - 需求分析

在正式開始實作前，盤整整個專案功能實現的目的與方式:

功能|說明|實作方式
---|---|---
建立會員(卡)|配發每個會員一組UID，以供識別|SQL
修改會員資料|修改UID對應的會員資料|SQL
儲值紀錄|紀錄金流出入流程|SQL
儲值金額|儲值會員卡餘額|SQL
消費金額|對應訂單系統、後台系統，降低餘額|SQL
商品訂購|查詢庫存、品項ID|SQL
訂單出貨|消耗庫存、扣款|SQL
前端顯示|提供功能參數、輸入動作|Web or LineBot
後端處理|實作功能、SQL查詢、金流API串接|Python

### 資料庫結構

- User
  - UID
  - User Type
  - 客戶名稱
  - 密碼(加密方式還在想)
  - 其他個資
- Card log
  - 金流流水號
  - 功能使用(儲值 or 消費)
  - 成立(True or False)
  - 來源
- Order
  - 出貨單流水號
  - 詳細訂單資料...
  - 是否成立(允許出貨)
  - 是否完成(客戶已確認收到)

### 前端實作

目前規劃用LineBot或是搭建簡單的Web網站來進行

### 後端實作

使用Python串接各種功能(接收前端參數，功能調用，排程處理)

今天大概先這樣，明天將進行資料庫搭建作業~~絕對不是偷懶~~

## [day9] 建置SQL DB

使用sqlite3建置一個本機資料庫，當然要用mssql或自己掛Docker DB也可以

### 初始化資料庫

暫時先行，可能後續再依據實際開發狀況修改，以下為資料庫結構創建SQL

```sql
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Users" (
	"UID"	INTEGER NOT NULL UNIQUE,
	"TYPE"	INTEGER NOT NULL,
	"NAME"	TEXT NOT NULL,
	"PWDHASH"	TEXT NOT NULL,
	PRIMARY KEY("UID" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Cards" (
	"CID"	INTEGER NOT NULL UNIQUE,
	"Bind_User"	INTEGER,
	"Balance"	INTEGER NOT NULL DEFAULT 0,
	"Frozen"	INTEGER NOT NULL DEFAULT 0,
	PRIMARY KEY("CID" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "transmit_logs" (
	"ID"	INTEGER NOT NULL UNIQUE,
	"TYPE"	INTEGER NOT NULL DEFAULT 0,
	"STATUS"	INTEGER NOT NULL DEFAULT 0,
	"Remark"	TEXT,
	PRIMARY KEY("ID" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Order_logs" (
	"ID"	INTEGER NOT NULL UNIQUE,
	"TID"	INTEGER,
	"Valid"	INTEGER NOT NULL DEFAULT 0,
	"Shipment_Status"	INTEGER NOT NULL DEFAULT 0,
	"Order_INFO"	TEXT,
	PRIMARY KEY("ID" AUTOINCREMENT)
);
COMMIT;
```

### 使用Python調用sqlite3

#### 載入資料庫

如果目標路徑沒有檔案，會建立一個新的.DB檔案

```python
import sqlite3 as db
conn = db.connect(env['SQL']['sqlite_URL'])
print(f"load database from {env['SQL']['sqlite_URL']} successfully")
```

#### 初始化資料庫(執行SQL檔案)

讀取SQL檔案並執行

```python
def exec_sqlfile(conn, fp):
    try:
        with open(fp, 'r') as sql_file:
            sql_script = sql_file.read()
        cursor = conn.cursor()
        cursor.executescript(sql_script)
        conn.commit()
        conn.close()
        print("Execte Script successfully")
        return True
    except Exception as err:
        print(err)
        return False

exec_sqlfile(conn=conn, fp="./data/sql/init.sql")
```

#### 新增一個測試帳號(插入資料至指定Table)

sqlite3的佔位符是**?**

格式為cursor.execute(str of sqlscript, (變數))，可以[參考](https://docs.python.org/zh-tw/3/library/sqlite3.html#using-sqlite3-efficiently)

```python
def INS_user(conn, user):
    try:
        sql = f"INSERT INTO Users (TYPE, NAME, PWDHASH) VALUES (?, ?, ?)"
        cursor = conn.cursor()
        cursor.execute(sql, (user.type, user.name, user.pwdhash),)
        uid = cursor.lastrowid
        conn.commit()
        conn.close()
        print(f"Execte INSERTR user successfully:{uid}")
        return uid
    except Exception as err:
        print(err)
        return -1
```

#### 查詢User資料(SELECT from Table)

藉由UID查詢User Table中的紀錄

```python
def quy_user(conn, uid):
  sql = f"SELECT * FROM Users WHERE UID = {uid}"
  print(sql)
  for row in conn.execute(sql):
      print(row)
```

這邊寫的比較急，剛烤肉回來月半中，後續可能會再慢慢追加forign key與其他資料庫設計，先這樣能用就好

## [day10] Flask Python API Service

安裝Flask跟套件

```pwsh
pip install flask
pip install flask-restful
```

### 設定測試API

雖然使用sqlite時應該不會有連線問題，不過在這邊還是簡單寫一個測試執行SQL的Route，如果執行成功顯示Database ONLINE

將伺服器掛載在http的port 8080上，在/dbstatus以GET方式接收請求

```python
# Server.py
import util.dbcc as dbcc

app = flask.Flask(__name__)
api = Api(app)

@app.route("/dbstatus", methods=['GET'])
def HelloWorld():
    if(dbcc.quy_dbonline(conn)):
        return "Database ONLINE"
    else:
        return "Database OFFLINE"

if __name__ == '__main__':
    env = ConfigParser()
    env.read('env.ini')
    try:
        conn = db.connect(env['SQL']['sqlite_URL'], check_same_thread=False)
        print(f"load database from {env['SQL']['sqlite_URL']} successfully")
        app.run(port = 8080, debug=True)
    except Exception as err:
        print(err)
```

後續將以Server.py作為整個專案的中控主程式，對接API

## day[11] Hello Line - 第一個Line訊息

本次鐵人賽將通過Line機器人搭建專案，所以沒有[Line Developers](https://developers.line.biz/en/)的快去申請吧，會用到的是[Messaging API](https://developers.line.biz/console/channel/new?type=messaging-api)在註冊完成後請安裝需求套件

```bash
pip install line-bot-sdk
pip install pyjwt
pip install jwcrypto
pip install cryptography
```

### 產生 Assertion Signing Key(KID)

本次專案以[channel access tokens v2.1](https://developers.line.biz/en/docs/messaging-api/generate-json-web-token/)版本進行實作，依照要求，需要[產生Assertion Signing Key](https://developers.line.biz/en/docs/messaging-api/generate-json-web-token/#create-an-assertion-signing-key)

按照官網文件說明，因為只需要進行一次，可以透過瀏覽器開發工具快速的產生，或者使用Python也可以，這邊使用Google瀏覽器，按下F12開啟開發者工具，選擇Console頁籤，將以下程式碼貼上，即會產生private key與public key

```javascript
(async () => {
  const pair = await crypto.subtle.generateKey(
    {
      name: 'RSASSA-PKCS1-v1_5',
      modulusLength: 2048,
      publicExponent: new Uint8Array([1, 0, 1]),
      hash: 'SHA-256'
    },
    true,
    ['sign', 'verify']
  );
   
  console.log('=== private key ===');
  console.log(JSON.stringify(await crypto.subtle.exportKey('jwk', pair.privateKey), null, '  '));
   
  console.log('=== public key ===');
  console.log(JSON.stringify(await crypto.subtle.exportKey('jwk', pair.publicKey), null, '  ')); 
})();
```

將產生的**public key**貼到[Line Developers Console](https://developers.line.biz/console/)創建的channels中的Assertion Signing Key欄位，如果看到右側有一串字串出現代表成功了，這就是KID，存起來等等會用到

### 實作取得JWT

Line使用[JWT](https://jwt.io/#libraries-io)，並以此簽名Token，詳細加密原理請參照網站

此處產生Token的方式需要準備以下參數:

Property|說明
---|---
kid|將Public Key填入網站後右側的字串
iss|Channel ID
sub|Channel ID
aud|<https://api.line.me/>
exp|JWT的有效期限
token_exp|以本JWT簽名的Token的有效期限

以Python實作:

```python
import jwt
from jwt.algorithms import RSAAlgorithm
import time

privateKey = {
  "alg": "RS256",
  "d": "dcA-LXLBRecBQbW7a8LKAriFJhnpXzwu2uNoVF_8-QmGVzI5682FWh_CWhl_B6J0fpmA-d7_EP0WCB3AGhxlyTP6ROoYJo7nygb_KMLREM7n64LFGbvNtw4jk7dmISXl_JuEX6CG09BBx4GLh9AGHSaK4v9B-dDvrNZlAo2mIjISHNcAPENbOl_XIOmZpJd56znjjc1gGKaYGbIm8unxHnPhL66IVYGRu8gxKfG6JUP7o370-VDfFOeaAR0HshTycP6M41jcDSjL6z9-J-Sh0zSZXqGS4u82TNtmwtRTzVwd0w30KQ0TTROTiNsz5apVHjpMvmAxRlbvcW41xIq8sQ",
  "dp": "PAWBMzwnwgc-yixarV30gemH6Wk15HfSUYpR4wJZUHemGx_LE5GXdnKoyy8G9DAl6XMpm7YVH8cPXgXYNh-JlAggvzUeH5A7KAV4ZPTNak4CI844GSbYIu_dPBcVAg0O6sxQWugYpPbPnMDpE7qf4KilSSVG3JKqEMxkYySjZZE",
  "dq": "LBA_q2YYnglCL41-1b3BmzCm-hs7Q-N__otDWO01I03VYnzU-vEQmxy6Fzrh2Y4Fgwp6D8iScu42AOyhE-T-qDNbAsCB0iZeFqm84g6VQAfDbknjIUZtcGvQgzy-zlrl253_QdyJvl2b44KT1hfoF0tDNA1rhOy7WlBM__rH0Pc",
  "e": "AQAB",
  "kty": "RSA",
  "n": "x2glWJ7baQV4vdElnAXA5yu8yFk4LpszkHW3Ey-BKGT3kGVLy3Jk3OvkwjBFOglXWeyTWe_rJkMYkBKuon5syZVjrjb24CmViAXGr6d6IvrYWj8IGZ6ElVABfnjGgZMVywmBb7hIh2p8QR0L8UJEuWjBU5nlwkMBpvnY2HXAVhvir8CN7WRj_GBMxxgg7wSuW1tV-7Qf44grMqJ0Je7zjflS4-TpI8Ox3nhamn0d7NIdQ3jNdTP7IZF61IvETgb_6NdFnfsN-aifJC-Ea3ZwhVcEGJ5z3MMoKSoChJmkJMiV9CldqGRnEDWwBugZHeEtn71eGVE3DAXAzrf525YHYQ",
  "p": "7eH8LAzNkITH6t7CWU5tPAmQlGQPkby66Yfq52tSZ43pQRz0CdtDYCQnGoBXvHzAHhzH4MjmNLOSGVimZK_dIRg5lJaPvVe6hgQ3pYud5WzPWsnQTsC7agQ2rfQglyFUtjwd1gWBIY4gwHj4BYG6Up3g0TlX1sf_juZxcLhkOsc",
  "q": "1pf-Pj2ZPL1nGqVcMVH_hfziIOBtjxc5vMGyHwTaLAA9y2xKfe_SRU8kUK2q5ZykJ8wMckR9Pduuyn-vp4q2FANVSN69G01pUKM2ppkgXuil2S3REmzniGdajZjkpWKaZ6z1tJ_xSv9ghx06Dbro8n___KnpBq6afb022anRxJc",
  "qi": "6L6SgH_pkyqq1Tb6QXPAGmtqVZT58Ljf3QTw6Tx5OdZ9NNvDReHHb64MgbUMLhLzGMeXGqDI5j0WLhtXv4ddCKWkF7OeKLUNuRP7yLpyYMazn8TEOjKHsgLAklenxcSgYaoO_wULh1mze1_ZO2PJNgvkIx_Xzr0XDUAqUp4W0jk",
  "use": "sig"
}

headers = {
    "alg": "RS256",
    "typ": "JWT",
    "kid": "9869e446-3489-4516-a83f-ec9214ad94d0"
}

payload = {
  "iss": "1234567890",
  "sub": "1234567890",
  "aud": "https://api.line.me/",
  "exp":int(time.time())+(60 * 30),
  "token_exp": 60 * 60 * 24 * 30
}

key = RSAAlgorithm.from_jwk(privateKey)

JWT = jwt.encode(payload, key, algorithm="RS256", headers=headers, json_encoder=None)
print(JWT)
```

### 實作取得channel_access_token

在這邊，要向Line官方取得token，在產生JWT後，需要在JWT的有效期限內進行token的產生，詳細的錯誤說明與欄位解釋可以參照[官方文件](https://developers.line.biz/en/reference/messaging-api/#issue-channel-access-token-v2-1)，會使用到的參數如下:

Property|說明
---|---
JWT|JWT，JSON格式

以Python實作:

```python
def Issue_channel_access_token(JWT):
  #https://developers.line.biz/en/reference/messaging-api/#issue-channel-access-token-v2-1
  url = "https://api.line.me/oauth2/v2.1/token"
  headers = APIPm.xwwwformurlencodedheaders
  data = {
      "grant_type":"client_credentials",
      "client_assertion_type":"urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
      "client_assertion": JWT
  }
  resp = APIPm.sendreq(url=url, headers=headers, data=data)
  # resp = json.loads(resp.text)
  return jsonresphandler(resp)
```

### Hello Line，發送訊息

有了Token，就可以進行API的使用了，這邊先跳到Line Developers，請在自己的機器人的Basic setting中最下方找到**Your user ID**存起來備用，要發訊息囉

以Python實作:

```python
def Send_push_message(token, IDs):
  access_token = token['access_token']
  url = "https://api.line.me/v2/bot/message/push"
  headers = APIPm.jsonheaders.copy()
  headers['Authorization'] = f"Bearer {access_token}"
  data = {
      "to": IDs,
      "messages":[
          {
              "type":"text",
              "text":"Hello, world"
          },
          {
              "type":"text",
              "text":"Hello, ITironman"
          }
      ]
  }
  resp = APIPm.sendreq(url=url, headers=headers, data=json.dumps(data, indent=4))
  return jsonresphandler(resp)
```

現在應該可以在手機上找到發給自己的訊息了，明天開始把接收功能做出來

## [day12]Heroku 基本使用

如果你有自己的固定IP，可以在本機進行部署，或著使用免費版本的[Heroku Platform](https://devcenter.heroku.com/)在雲端建立你的伺服器，方法沒有一定，今天進行Python版本的建置流程

### 套件安裝

在[這邊](https://signup.heroku.com/signup/dc)建立你的Heroku Free Account

安裝[Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)

### 下載並啟用範例專案

```cmd
git clone https://github.com/heroku/python-getting-started.git
cd python-getting-started
```

如果你因為設定錯了參數，想要重新使用已經創建的App，可以使用以下指令設定遠端專案

```git
heroku git:remote -a [the-app-name]
```

### 建立第一個Heroku App

建立一個新App，並將當前的專案推送至Heroku

```sh
heroku create
git push heroku main
```

建置完成的App，在**未啟用**前處於壓縮的狀態(slug)，將其部屬到節點([dynos](https://devcenter.heroku.com/articles/dynos))，才能啟用App，使用以下指令分配一個dynos給App:

```sh
heroku ps:scale web=1
```

完成資源分配後，你的App就能夠使用分配到的資源開始運作，使用以下指令測試App:

```sh
heroku open
```

檢視Log:

```sh
heroku logs --tail
```

### Procfile

[Procfile](https://devcenter.heroku.com/articles/procfile)，是App的啟動指令，格式為

```python
<process type>: <command>
# 測試App中的Procfile為
web: gunicorn gettingstarted.wsgi
```

只有web類型的程序能夠進行HTTP傳輸，其他類型的則無法從Heroku的Router上接收傳送資料

### requirements環境套件

如果專案根目錄存在requirements.txt，Heroku將會判斷專案為Python語言，同時在部署時Heroku會讀取內部的內容安裝指定的套件

如果你沒有虛擬環境，或虛擬環境有太多不相干的套件，可以使用pipreqs產生專案的requirements.txt

```sh
pip install pipreqs
pipreqs /path/to/project
```

### 本機運行測試

在部署上去之前，可以在個人電腦進行模擬測試，以避免上船上去後發生編譯錯誤或其他問題，由於是本機運作，如果系統為Windows需要設定專用的Procfile:

```Procfile
# Procfile.windows
python manage.py collectstatic

#以此指令在Windows上啟動本機模式
heroku local web -f Procfile.windows

#以此指令在Unix系統上執行本機模式
heroku local web
```

使用瀏覽器打開<http://localhost:5000>，如果正常，應該可以看到App產生的網頁

### 將修改完成的新版本上傳到雲端

Heroku使用與Git同樣的格式進行版本控管，以下為範例

修改requirements.txt，新增reequests套件使用

在hello/views.py加入import requests，並修改index函式為:

```python
def index(request):
    r = requests.get('http://httpbin.org/status/418')
    print(r.text)
    return HttpResponse('<pre>' + r.text + '</pre>')
```

完成本機測試後，與Git相同

```sh
git add . 
git commit -m "new Index"
```

部署

```sh
git push heroku main
```

開啟

```sh
heroku open
```

### 設定環境變數

Heroku鼓勵使用[config vars](https://devcenter.heroku.com/articles/config-vars)作為變數的儲存方式，可以通過網頁的控制台頁籤中的Setting-Config Vars進行設定，或使用CLI

```sh
#顯示專案環境變數
heroku config

#取得特定的變數值
heroku config:get [Key]

#設定環境變數
heroku config:set [Key]=[Val]

#移除環境變數
heroku config:unset [Key]
```

### 其他功能

[插件](https://devcenter.heroku.com/articles/what-is-an-add-on)、[執行命令、開啟Bash](https://devcenter.heroku.com/articles/one-off-dynos)

今天簡單的過一遍基礎的Heroku使用方式，明天進入將Line機器人部署的教學

## [day13] 設定gunicorn Logging

使用gunicorn作為HTTP Server的時候，必須手動指派gunicorn的logger作為flask的logger handler，才能夠正常的進行DEBUG、WARN、INFO、WARN、CRIT等的log紀錄

在Server.py內加入如下程式碼，以將gunicorn的logger與flask App結合

```python
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
```

### gunicorn log 使用方式

指定logging以debug模式運作，修改Procfile內指令為:

```Procfile
web: gunicorn --log-level=debug Server:app
```

logger的使用方式:

```python
# app.logger.[LEVEL]([LOG_MESSAGE])
app.logger.debug('this is a DEBUG message')
app.logger.info('this is an INFO message')
app.logger.warning('this is a WARNING message')
app.logger.error('this is an ERROR message')
app.logger.critical('this is a CRITICAL message')
```

在Server.py內加入一個新的route以測試log效果

```python
@app.route('/')
def default_route():
    """Default route"""
    app.logger.debug('this is a DEBUG message')
    app.logger.info('this is an INFO message')
    app.logger.warning('this is a WARNING message')
    app.logger.error('this is an ERROR message')
    app.logger.critical('this is a CRITICAL message')
    return jsonify('that's a log of logs')
```

完成所有修改後將修改部署到heroku，測試功能吧

```sh
git add .
git commit -m "logging"
git push heroku main
heroku open
herolu logs -t
```

使用herolu logs 查詢logs，你應該可以看到如下輸出

```log
2021-09-25T09:19:39.406667+00:00 app[web.1]: [2021-09-25 09:19:39 +0000] [7] [DEBUG] this is a DEBUG message
2021-09-25T09:19:39.406742+00:00 app[web.1]: [2021-09-25 09:19:39 +0000] [7] [INFO] this is an INFO message
2021-09-25T09:19:39.406816+00:00 app[web.1]: [2021-09-25 09:19:39 +0000] [7] [WARNING] this is a WARNING message
2021-09-25T09:19:39.406877+00:00 app[web.1]: [2021-09-25 09:19:39 +0000] [7] [ERROR] this is an ERROR message
2021-09-25T09:19:39.406935+00:00 app[web.1]: [2021-09-25 09:19:39 +0000] [7] [CRITICAL] this is a CRITICAL message
```

### 使用Heroku 模組以從網頁瀏覽logs

你可以通過[Papertrail](https://devcenter.heroku.com/articles/papertrail)進行App的狀態監測與查看logs，可以省去自行撰寫logs分類，與命令列方式查閱不易的問題，並提供各種如錯誤通知的功能

```sh
heroku addons:create papertrail
heroku addons:open papertrail
```

你可以通過如上addons:open指令開啟模組的網頁，或是直接以如下方式從瀏覽器直接進入，將<app name\>替換為你的heroku App名稱

```sh
https://addons-sso.heroku.com/apps/<app name>/addons/papertrail
```

今天補一點昨天沒有忘了補充的部分

## [day14] 接收使用者的Line訊息

結合先前的

1. 產生[channel access token](https://ithelp.ithome.com.tw/articles/10270875)
2. 設定[heroku](https://ithelp.ithome.com.tw/articles/10271516)

可以開始建立一個伺服器接收由Line官方送過來的資訊，此處假設你使用Heroku進行開發，在[Line Developers Console](https://developers.line.biz/console/)內，將Channel-->Messaging API-->Webhook URL設定為

https://[AppName].herokuapp.com/callback

並將Auto-reply messages 與 Greeting messages同樣設為Disabled，方法為:

1. 點選右側的Edit
2. Line Offficial Account Manager-->回應設定
3. 停用加入好友的歡迎訊息與自動回應訊息

### 實作並部署回聲機器人

此機器人功能:回傳傳給機器人的文字訊息

如果未安裝line-bot-sdk套件

```sh
pip install line-bot-sdk
```

修改Server.py，加入以下內容

```python
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os

app = Flask(__name__)
api = Api(app)

#LCAT為Channel Access Token
line_bot_api = LineBotApi(os.environ['LCAT'])

#Cst為Channel secret
handler = WebhookHandler(os.environ['Cst'])

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
```

部署:

```sh
git add .
git commit -m "Echo Bot"
git push heroku main
```

此時從Line傳訊息給機器人，你應該就可以收得到來自機器人的回訊

![line echo reply bot](readme/LINE-capture-654281712.289593.jpg)

#### 加機器人為好友

Line Developers --> Channel Setting --> Messaging API --> Bot information --> Bot basic ID or QR code

使用你的手機搜尋Bot basic ID或掃描QR code加機器人為好友

### 過程解析

這是一個由Line官方傳送過來的Webhook Sample

```json
{
  "destination": "xxxxxxxxxx",
  "events": [
      {
          "type": "message",
          "message": {
              "type": "text",
              "id": "14353798921116",
              "text": "Hello, world"
          },
          "timestamp": 1625665242211,
          "source": {
              "type": "user",
              "userId": "U80696558e1aa831..."
          },
          "replyToken": "757913772c4646b784d4b7ce46d12671",
          "mode": "active"
      },
      {
          "type": "follow",
          "timestamp": 1625665242214,
          "source": {
              "type": "user",
              "userId": "Ufc729a925b3abef..."
          },
          "replyToken": "bb173f4d9cf64aed9d408ab4e36339ad",
          "mode": "active"
      },
      {
          "type": "unfollow",
          "timestamp": 1625665242215,
          "source": {
              "type": "user",
              "userId": "Ubbd4f124aee5113..."
          },
          "mode": "active"
      }
  ]
}
```

1. 手機發訊息給Line
2. Line傳送通知給bot server(webhook URL)的[webhook]((https://developers.line.biz/en/reference/messaging-api/#webhooks)
3. WebhookHandler驗證headers中的**x-line-signature**欄位簽章，除了使用SDK進行驗證，也可以[手動進行驗證](https://developers.line.biz/en/reference/messaging-api/#signature-validation)
4. 將資料傳送給配對的執行函數，如本次範例中使用的MessageEvent與TextMessage，進行處理
5. 使用Line SDK回覆訊息，回傳TextSendMessage(text=event.message.text)) 以此範例還說，就是Hello, world

跑完接收與發送，之後要開始把功能逐漸拼起來組成專案了

## [day15]幾個常用的LineAPI

今天Heroku[大當機](https://status.heroku.com/incidents/2362)0rz，寫一點Line API的使用教學

LineSDK已經將大部分的實作功能與資料模型都包入了，這可以加快開發的速度:

```python
line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')
```

### 取得機器人資訊

```python
bot_info = line_bot_api.get_bot_info()

print(bot_info.display_name)
print(bot_info.user_id)
print(bot_info.basic_id)
print(bot_info.premium_id)
print(bot_info.picture_url)
print(bot_info.chat_mode)
print(bot_info.mark_as_read_mode)
```

### 推送、回覆訊息

回覆訊息

```python
line_bot_api.reply_message('<reply_token>', TextSendMessage(text='Hello World!'))
```

推送訊息

```python
try:
  line_bot_api.push_message('<to>', TextSendMessage(text='Hello World!'))
except LineBotApiError as e:
  # error handle
```

免費帳號有**單月500則**推送訊息的限制，回覆則不用錢

### 取得使用者資訊

在使用的時候，知道使用者的userid後，就能夠藉此取得使用者的顯示名稱(暱稱)、系統的使用語言、大頭貼、狀態消息，這可以提供一點使用者的資訊

```python
profile = line_bot_api.get_profile(user_id)

print(profile.display_name)
print(profile.user_id)
print(profile.picture_url)
print(profile.status_message)
```

這邊要注意一點，Line的JSON變數命名與Python不同，例如使用者ID，在Line送過來的Json body內以events.source.userID方式存放，但在Python，則為event.source.**user_id**，在資料變數命名上有許多的不同需要確認

### 取得使用者訊息中的非文字內容

如圖片、影片、音訊、檔案等

```python
message_content = line_bot_api.get_message_content(message_id)

with open(file_path, 'wb') as fd:
    for chunk in message_content.iter_content():
        fd.write(chunk)
```

### Line-SDK的意外處理

通常會是格式或參數錯誤，錯誤說明可以[參考](https://developers.line.biz/en/reference/messaging-api/#error-messages)

```python
try:
    line_bot_api.push_message('to', TextSendMessage(text='Hello World!'))
except linebot.exceptions.LineBotApiError as e:
    print(e.status_code)
    print(e.request_id)
    print(e.error.message)
    print(e.error.details)
```

今天主要在翻API文件，還有heroku在搞，明天會把對話紀錄生出來.....

## [day16]機器人對話紀錄

以前遇到一個情況阿，使用者輸入，我要ㄧ個漢堡，二杯奶茶，到後台卻變成，我要\xe3\x84\xa7個漢堡，二杯紅茶，截圖拍給我，很正常是ㄧ個漢堡，看了半天沒看出什麼鬼，最後發現

這個《ㄧ》個漢堡的一，是注音符號的《ㄧ》，你永遠不知道使用者會用什麼方式打字，在互動式的設計下，你會需要保留原始的對話紀錄，以應對各種神祕的輸入法所造成的問題，這邊要依據先前創建的Line Bot進行資料紀錄

### Postgres 初始化 & 連線

#### 新增Postgres模組到你的專案

使用[免費方案hobby-dev](https://devcenter.heroku.com/articles/heroku-postgres-plans#hobby-tier)

```sh
heroku addons:create heroku-postgresql:hobby-dev
```

用heroku pg:info檢查Postgres資料庫狀態

```sh
Plan:                  Hobby-dev
Status:                Available
Connections:           5/20
PG Version:            13.4
Created:               2021-09-27 02:30 UTC
Data Size:             8.1 MB/1.00 GB (In compliance)
Tables:                1
Rows:                  3/10000 (In compliance)
Fork/Follow:           Unsupported
Rollback:              Unsupported
Continuous Protection: Off
Add-on:                postgresql-dimensional-#####
```

#### 建立表格

可以使用[pgAdmin 4](https://www.pgadmin.org/)進行這個步驟，在dashboard內的addons，可以找到Heroku Postgres，Settings，Database Credentials會有從本機連線到資料庫的所需資訊

參數|填入Pgadmin欄位
---|---
Host|Connection -Host Name/Address
Database|Connection - Maintance Database & Advanced - DB Restriction
User|Connection - User
Port|Connection - Port
Password|Connection - Password

```sql
CREATE TABLE IF NOT EXISTS public.messaging_log
(
    id text COLLATE pg_catalog."default" NOT NULL,
    type text COLLATE pg_catalog."default" NOT NULL,
    text text COLLATE pg_catalog."default",
    datetime timestamp with time zone NOT NULL,
    source_uid text COLLATE pg_catalog."default" NOT NULL,
    source_type text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT messaging_log2_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;
```

#### 連線

如果你的App與Postgres在相同的專案下，在App內與資料庫連線時，你不需要特別設定資料庫連線的URL、使用者名稱、密碼等，在跨專案運作時請參考[官方文件](https://devcenter.heroku.com/articles/heroku-postgresql#sharing-heroku-postgres-between-applications)

安裝連線Driver

```sh
pip install psycopg2-binary
```

安裝完Addons你的Vars變數內會自動追加DATABASE_URL

```python
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
```

測試連線，看能否執行查詢資料庫版本指令

```python
cur = conn.cursor()
cur.execute('SELECT VERSION()')
rr = cur.fetchall()
app.logger.debug(f"DBver:{rr}")
# "Database Version: [('PostgreSQL 13.4 (Ubuntu 13.4-1.pgdg20.04+1) on x86_64-pc-linux-gnu, compiled by gcc (Ubuntu 9.3.0-17ubuntu1~20.04) 9.3.0, 64-bit',)]"
conn.commit()
cur.close()
```

### 紀錄Line對話

藉由解析[Webhook Event Objects](https://developers.line.biz/en/reference/messaging-api/#webhook-event-objects)可以從使用者的對話中取得如下資訊

1. 訊息類型
2. 訊息ID
3. 訊息文字(如果是文字訊息)
4. 訊息來源
5. 訊息來源使用者ID
6. 使用者的顯示名稱....
7. 以millisecond計算的Timestamp

```python
prof = line_bot_api.get_profile(event.source.user_id)
dt = datetime.fromtimestamp(event.timestamp / 1000.0).astimezone(TWT)
format_time = dt.strftime("%Y/%m/%d %H:%M:%S")
app.logger.debug(f"message:{event.message.type}-{event.message.id} = {event.message.text}, from {event.source.type}:{prof.display_name}({event.source.user_id}) at {format_time}")
# [DEBUG] message:text-<訊息ID> = 王大明愛吃漢堡包, from user:<使用者的顯示名稱>(<訊息來源使用者ID>_ at 2021/09/28 17:53:00
```

將對應的參數填入Sql變數

```python
def INS_msg_log(self, id, msgtype, text, dt, stype, suid):
  cur = self.conn.cursor()
  query = sql.SQL("INSERT INTO {}(id, type, text, datetime, source_uid, source_type) VALUES(%s, %s, %s, %s, %s, %s)").format(sql.Identifier('messaging_log'))
  cur.execute(query, (id, msgtype, text, dt, suid, stype))
  self.conn.commit()
  cur.close()

dbpm.INS_msg_log(event.message.id, event.message.type, event.message.text, dt.isoformat(), event.source.type, event.source.user_id)
```

如果運作正常，你就可以在資料庫查詢到每一筆使用者的訊息

訊息ID|訊息類型|訊息文字|時間(UTC)|UID|使用者類型
---|---|---|---|---|---
14999999999999|	text	|Apple |	2021-09-28 07:51:32.835+00|	Uxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|	user|
14999999999999|	text	|Banana |	2021-09-28 07:51:39.133+00|	Uxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|	user|
14999999999999|	text	|王大明愛吃漢堡包|	2021-09-28 09:53:00.274+00|	Uxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|	user|

### Summary

你有沒有注意到，使用者名稱如果想儲存的話，是不是每一筆訊息都要查詢一次，這樣對話量一多會頻繁的向Line官方送出API請求，很容易造成被Ban，明天做一個UID與名稱對應表格吧

## [day17]使用者名稱表格

一樣先從建立表格開始，這張表格除了儲存來自Line的使用者資訊，也預留了未來資料的輸入欄位

欄位|說明
---|---
uid|Line使用者ID
displayName|Line顯示名稱
language|zh-hant、en-us....
pictureUrl|使用者大頭貼
FirstName|名
LastName|姓
phoneNumber|電話
Address|地址
Activate|啟用

```sql
CREATE TABLE IF NOT EXISTS public.customers
(
    uid text COLLATE pg_catalog."default" NOT NULL,
    "displayName" text COLLATE pg_catalog."default" NOT NULL,
    language text COLLATE pg_catalog."default",
    "pictureUrl" text COLLATE pg_catalog."default",
    "FirstName" text COLLATE pg_catalog."default",
    "LastName" text COLLATE pg_catalog."default",
    "phoneNumber" text COLLATE pg_catalog."default",
    "Address" text COLLATE pg_catalog."default",
    "Activate" boolean DEFAULT true,
    CONSTRAINT customers_pkey PRIMARY KEY (uid)
)

TABLESPACE pg_default;
```

### 實作紀錄使用者資訊

```python
def INS_UPD_cus(self, prof):
    # display_name (str) – Display name
    # user_id (str) – User ID
    # picture_url (str) – Image URL
    # status_message (str) – Status message
    # language (str) – Get user’s language

    cur = self.conn.cursor()
    query = sql.SQL("SELECT 1 AS isExists FROM {} WHERE uid = %s").format(sql.Identifier('customers'))
    cur.execute(query, ([prof.user_id]))
    r = cur.fetchone()
    cur.close()

    if(not r):
        cur = self.conn.cursor()
        query = sql.SQL("INSERT INTO {}(uid, \"displayName\", language, \"pictureUrl\") VALUES(%s, %s, %s, %s)").format(sql.Identifier('customers'))
        cur.execute(query, (prof.user_id, prof.display_name, prof.language, prof.picture_url))
        self.conn.commit()
        app.logger.debug(f"New User:{prof.display_name} - {prof.user_id}, Created")
        cur.close()
        return 1
    else:
        cur = self.conn.cursor()
        query = sql.SQL("UPDATE {} SET \"displayName\"=%s, language=%s, \"pictureUrl\"=%s, \"Activate\"=%s WHERE uid = %s").format(sql.Identifier('customers'))
        cur.execute(query, (prof.display_name, prof.language, prof.picture_url, "TRUE", prof.user_id))
        self.conn.commit()
        app.logger.debug(f"User:{prof.display_name} - {prof.user_id}, UPDATED")
        cur.close()
        return 2

prof = line_bot_api.get_profile(event.source.user_id)
INS_UPD_cus(prof)
```

在WebhookHandler被呼叫時，會依據訊息中的user_id搜尋資料庫，如果沒有這個Line UID，則會新增這個新使用者，反之如果是既有用戶，則會更新資料庫中使用者的顯示名稱等資訊

#### Postgresql採到的坑

```sql
query = sql.SQL("INSERT INTO {}(uid, \"displayName\", language, \"pictureUrl\") VALUES(%s, %s, %s, %s)").format(sql.Identifier('customers'))
```

為什麼UID不用加雙引號「"」，displayName要加，language卻又不用加，下一個pictureUrl又要加雙引號，答案是**大小寫**，如果你在postgresql中建立了帶有大小寫的欄位名稱，請務必要加上雙引號，這困擾了我快2個小時找錯誤.....

## [day18] 追蹤 & 封鎖事件處理
