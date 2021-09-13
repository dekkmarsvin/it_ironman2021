from types import SimpleNamespace

def ReqOrderCreate(ShopNo = "", OrderNo = "", Amount = 0, CurrencyID = "TWD", PrdtName = "", Memo = "", \
        Param1 = "", Param2 = "", Param3 = "", ReturnURL = "", BackendURL = "", PayType = "", ExpireDate = "", \
            AutoBilling = "Y", ExpBillingDays = 14, ExpMinutes = 10, PayTypeSub = "ONE"):
    # 永豐銀行- 數位金流 API 技術規格文件 page 32
    return SimpleNamespace(ShopNo = ShopNo, OrderNo = OrderNo, Amount = Amount, CurrencyID = CurrencyID, PrdtName = PrdtName, Memo = Memo, \
        Param1 = Param1, Param2 = Param2, Param3 = Param3, ReturnURL = ReturnURL, BackendURL = BackendURL, PayType = PayType, ATMParam = SimpleNamespace(ExpireDate = ExpireDate), \
            CardParam = SimpleNamespace(AutoBilling = AutoBilling, ExpBillingDays = ExpBillingDays, ExpMinutes = ExpMinutes, PayTypeSub = PayTypeSub))

def ReqOrderQuery(ShopNo = "", OrderNo = "", PayType = "", OrderDateTimeS = "", OrderDateTimeE = "", PayDateTimeS = "", \
        PayDateTimeE = "", PayFlag = "", ):
    # 永豐銀行- 數位金流 API 技術規格文件 page 38
    return SimpleNamespace(ShopNo = ShopNo, OrderNo = OrderNo, PayType = PayType, OrderDateTimeS = OrderDateTimeS, OrderDateTimeE = OrderDateTimeE, \
        PayDateTimeS = PayDateTimeS, PayDateTimeE = PayDateTimeE, PayFlag = PayFlag)