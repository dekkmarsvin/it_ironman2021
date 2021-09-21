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
