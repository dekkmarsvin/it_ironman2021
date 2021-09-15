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
- 付款完成頁面:https://0.0.0.0/store/Return
- 主機端:https://0.0.0.0/bakcend
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
