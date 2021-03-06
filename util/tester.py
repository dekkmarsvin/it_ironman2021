import argparse
import os
from re import L
from linebot import LineBotApi
from linebot.models import (
    RichMenu, RichMenuArea, RichMenuResponse, RichMenuSize, RichMenuBounds, URITemplateAction, URIAction, PostbackAction, MessageAction
)
from dbPm import DBPm
from util import APIModel
from util import GenApi
from util import linecc

dblist = ['cart_items', 'coupon', 'customers', 'messaging_log', 'orders', 'payment_log', 'product_category', 'products', 'shopping_cart']
LineApiList = ['rich_menu_create', 'rich_menu_img_upload', 'show_rich_menu_list', 'set_default_rich_menu', 'cancel_default_rich_menu', \
            'get_default_rich_menu', 'delete_rich_menu']

def askyes():
    val = input("Confirm to Do(Y/N):").lower()
    if(val == 'y' or val == 'yes'):return True
    else:return False

def init_product_category(dbpm:DBPm, yes=False):
    if(not yes):yes = askyes()
    if(not yes):return False

    drink_cate = ['酒','茶','果汁','碳酸飲料','咖啡','其他']
    drink_decp = ['酒（英語：Alcoholic beverage），其中含有0.5%至96%的酒精（即乙醇）。為人類飲用歷史最長的加工飲品之一，由植物發酵製成。', \
                '茶，是指利用茶樹的葉子所加工製成的飲料，多烹[3]成茶湯飲用，也可以加入食物中調味，也可入中藥使用。[4]現代的茶按製作工序主要分爲六大類，綠茶、白茶、黃茶、青茶、紅茶、黑茶[5]。茶大多種植在梯田(為了灌溉方便)。', \
                '蔬果汁，常簡稱果汁，是指從新鮮水果或蔬菜榨汁而成的一種飲料。', \
                '碳酸飲料又稱汽水，是充入二氧化碳氣體的軟性飲料，其中包括日常汽水，如七喜、可樂、碳酸水及沙士、麥根沙士雪碧等。', \
                '咖啡（英語：coffee）是采經過烘焙過程的咖啡豆（咖啡屬植物的種子）所製作沖泡的飲料。', \
                '如牛奶、豆漿、蜂蜜水、氣泡水、運動飲料等.....']
    for dc, de in zip(drink_cate, drink_decp):
        try:
            dbpm.INS_Prod_Cat(dc, de)
        except Exception as Err:
            print(Err)
            return False
    return True

def init_products(dbpm:DBPm, yes=False):
    if(not yes):yes = askyes()
    if(not yes):return False

    drink_products = ['可口可樂Zero易開罐330ml(24入)', '可口可樂-易開罐330ml (24入/箱)', '【味丹】激浪汽水-冰晶檸檬風味', '七喜汽水330ml(24入)', '百事可樂 250ml(24入)']
    drink_quantity = [99,98,97,96,95]
    drink_product_decp = ['此品新舊包裝隨機出貨，如可接受再購買', '新舊包裝隨機出貨，如可接受再購買', '清爽透明系 減糖少負擔\n清新檸檬萊姆風味\n順暢氣泡 瞬間振奮', \
                        '★清涼暢快\n★檸檬口味', '★Dare for more\n★渴望、探索、創造']
    drink_product_s_time = []
    drink_product_e_time = []
    for i in range(len(drink_products)):
        if(i<=1):
            st, et = dbpm.timedelta_bydays()
            drink_product_s_time.append(st)
            drink_product_e_time.append(et)
        else:
            st, et = dbpm.timedelta_bydays(days=730)
            drink_product_s_time.append(st)
            drink_product_e_time.append(et)
    drink_product_cate = '碳酸飲料'
    drink_product_price = [288, 288, 519, 309, 249]

    for dp,dq,de,dst,det,dpi in zip(drink_products, drink_quantity, drink_product_decp, drink_product_s_time, drink_product_e_time, drink_product_price):
        try:
            dbpm.INS_Prod(dp, dq, de, dst, det, drink_product_cate, dpi)
        except Exception as Err:
            print(Err)
            return False
    return True

def add_shopping_cart(dbpm:DBPm, id=os.environ['Me'], yes=False):
    try:
        id = input(f"輸入Line UID({id}):") or id
        if(not yes):yes = askyes()
        if(not yes):return False
        scid = dbpm.INS_QUY_SC(id)
        print(f"購物車ID:{scid}")
    except Exception as err:
        print(err)
        return False
    return True

def init_add_test_items_to_shopping_cart_via_lineuid(dbpm:DBPm, id=os.environ['Me'], yes=False):
    if(not yes):yes = askyes()
    if(not yes):return False

    cart_item_pid = [21, 23, 25]
    cart_item_qut = [3, 999, 9]

    try:
        print(f"line id:{id}")
        scid = dbpm.INS_QUY_SC(id)
        for cp, cq in zip(cart_item_pid, cart_item_qut):
            current_product_stocks = dbpm.QUY_Prod_Quantity_by_pid(cp)
            print(f"產品{cp}, 庫存:{current_product_stocks}")
            if(current_product_stocks - cq >= 0):
                print(f"INS, {cp} x {cq} to cart:{scid}")
                dbpm.INS_Prod_to_Cart(scid, cp, cq)
            else:
                print("庫存不足")
    except Exception as err:
        print(err)
        return False
    return True

def init_orders(dbpm:DBPm, id=os.environ['Me'], yes=False):
    if(not yes):yes = askyes()
    if(not yes):return False

    scid = dbpm.INS_QUY_SC(id)
    print(f"檢查購物車:{scid}")

    o_flag = True
    prodlist = []
    tot_price = 0

    shopping_list = dbpm.QUY_Shopping_Cart_by_scid(scid)
    if(not shopping_list):
        return False
    for prod in shopping_list:
        # print(f"商品:{prod[0]}, 數量:{prod[1]}")
        current_quantity = dbpm.QUY_Prod_Quantity_by_pid(prod[0])
        if(current_quantity - prod[1] < 0):
            dbpm.UPD_Cart_items(scid, prod[0], current_quantity)
            o_flag = False
        else:
            new_quantity = current_quantity - prod[1]
            dbpm.UPD_Prod_Quantity(prod[0], new_quantity)
            product_name, product_price = dbpm.QUY_Prod_Name_and_Price_by_pid(prod[0])
            prodlist.append(f"{product_name} * {prod[1]}")
            tot_price = tot_price + product_price * prod[1]
    if(not o_flag):
        return False

    # 鎖定購物車 
    dbpm.UPD_Shopping_Cart_lock_bY_scid(True, scid)

    # 建立訂單
    oid = dbpm.INS_Order(os.environ['Me'], scid, ostatus="初始化訂單")

    # 建立信用卡付款交易編號
    paid = dbpm.INS_payment_req('C-1', tot_price)
    neworder = APIModel.ReqOrderCreate(ShopNo=os.environ['ShopNo'], OrderNo=oid, Amount=tot_price*100, \
        PrdtName='IT鐵人賽虛擬商店', ReturnURL=os.environ['ReturnURL'], BackendURL=os.environ['BackendURL'], PayType="C")
    msg = GenApi.OrderCreate(neworder)
    print(msg)

    if(msg):
        if(msg.Status == 'S'):
            print(f"建立訂單: 編號:{msg.OrderNo}:{prodlist}, 請款金額 = {tot_price}, 付款ID:{paid}, {msg.Description}", {msg.CardParam.CardPayURL})
            dbpm.UPD_payment_bypaid(paid=paid, tsno=msg.TSNo, ts_decp=msg.Description, ts_status=True, cardpayurl=msg.CardParam.CardPayURL)
            dbpm.UPD_Order_by_oid(paid=paid, ostatus="已產生付款請求", oid=oid)
            return True
        else:
            dbpm.UPD_payment_bypaid(paid=paid, tsno=msg.TSNo, ts_decp=msg.Description, ts_status=False, cardpayurl=msg.CardParam.CardPayURL)
            dbpm.UPD_Order_by_oid(paid=paid, ostatus="產生付款請求失敗", oid=oid)
    return False

def add_product_category(dbpm:DBPm, yes=False):
    try:
        cate = input("商品類別:")
        decp = input("商品類別說明:")
        if(not yes):yes = askyes()
        if(not yes):return False
        dbpm.INS_Prod_Cat(cate, decp)
    except Exception as Err:
        print(Err)
        return False
    return True

def add_products(dbpm:DBPm, yes=False):
    try:
        p_name = input("商品:")
        p_quantity = input("商品庫存:")
        p_decp = input("商品說明:")
        daydiff = int(input("剩餘有效天數:"))
        p_st, p_et = dbpm.timedelta_bydays(days=daydiff)
        p_cate = input("商品類別:")
        p_price = int(input("價格:"))
        if(not yes):yes = askyes()
        if(not yes):return False
        dbpm.INS_Prod(p_name, p_quantity, p_decp, p_st, p_et, p_cate, p_price)
    except Exception as Err:
        print(Err)
        return False
    return True

def doinit(dbpm:DBPm, args):
    r = False
    if(args.target == 'product_category'):
        print("插入product_category測試資料")
        r = init_product_category(dbpm=dbpm, yes=args.yes)
    elif(args.target == 'products'):
        print("插入products測試資料")
        r = init_products(dbpm=dbpm, yes=args.yes)
    elif(args.target == 'cart_items' or args.target == 'shopping_cart'):
        print("插入購物車 & 插入購物車項目")
        r = init_add_test_items_to_shopping_cart_via_lineuid(dbpm=dbpm, yes=args.yes)
    elif(args.target == 'orders'):
        print("建立測試訂單")
        r = init_orders(dbpm=dbpm, yes=args.yes)
    if(r):print("成功")
    else:print("失敗")

def doadd(dbpm:DBPm, args):
    r = False
    if(args.target == 'product_category'):
        print("手動插入product_category資料")
        r = add_product_category(dbpm=dbpm, yes=args.yes)
    elif(args.target == 'products'):
        print("手動插入products資料")
        r = add_products(dbpm=dbpm, yes=args.yes)
    elif(args.target == 'shopping_cart'):
        print("手動插入購物車shopping_cart")
        r = add_shopping_cart(dbpm=dbpm, yes=args.yes)
    if(r):print("成功")
    else:print("失敗")

def add_upload_rich_menu_img(line_bot_api:LineBotApi, fp:str="./template/rm_01.png", yes=False):
    richmenuid = input("RichMenuId:")
    if(not richmenuid):return False
    fp = input(f"Default({fp}) or Enter:") or fp
    isvalid = os.path.exists(fp)
    print(f"Try load rich menu image from {fp}.....{isvalid}")
    if(not isvalid):return False
    if(not yes):yes = askyes()
    if(not yes):return False
    return linecc.Upload_Rich_Menu(line_bot_api, fp, richmenuid)

def init_default_rich_menu(line_bot_api:LineBotApi, yes=False):
    if(not yes):yes = askyes()
    if(not yes):return False
    areas = [RichMenuArea(
                bounds=RichMenuBounds(x=0, y=0, width=512, height=512),
                action=PostbackAction(
                    label="顯示購物車內容",
                    data="action=ShowProductList?pcid=16",
                    display_text="查詢早餐"
                )
            ),
            RichMenuArea(
                bounds=RichMenuBounds(x=512, y=0, width=512, height=512),
                action=PostbackAction(
                    label="顯示購物車內容",
                    data="action=ShowProductList?pcid=17",
                    display_text="查詢午餐"
                )
            ),
            RichMenuArea(
                bounds=RichMenuBounds(x=1024, y=0, width=512, height=512),
                action=PostbackAction(
                    label="顯示購物車內容",
                    data="action=ShowProductList?pcid=10",
                    display_text="查詢飲料"
                )
            ),
            RichMenuArea(
                bounds=RichMenuBounds(x=0, y=512, width=512, height=512),
                action=MessageAction(label="按下問號按鈕", text="顯示操作說明")
            ),
            RichMenuArea(
                bounds=RichMenuBounds(x=512, y=512, width=512, height=512),
                action=PostbackAction(
                    label="顯示購物車內容",
                    data="action=ShowShoppingCartContents",
                    display_text="我的購物車內有什麼"
                )
            ),
            RichMenuArea(
                bounds=RichMenuBounds(x=1024, y=512, width=512, height=512),
                action=PostbackAction(
                    label="查詢訂單",
                    data="action=ShowOrderStatus",
                    display_text="查詢訂單"
                )            
            )
        ]
    richmenuid = linecc.Create_Rich_Menu(line_bot_api, 1536, 1024, "default_Rich_Menu", "主選單", areas)
    print(f"rich_menu_id :{richmenuid}")
    if(richmenuid):return True
    else:return False

def info_get_rich_menu_list(line_bot_api:LineBotApi):
    rich_menu_list = linecc.get_rich_menu_list(line_bot_api)
    print(rich_menu_list)
    if(rich_menu_list):return True
    else:return False

def add_set_default_rich_menu(line_bot_api:LineBotApi, timeout=None, yes=False):
    rich_menu_id = input("Rich Menu ID:")
    if(not yes):yes = askyes()
    if(not yes):return False
    line_bot_api.set_default_rich_menu(rich_menu_id)
    return True

def del_delete_rich_menu(line_bot_api:LineBotApi, timeout=None, yes=False):
    rich_menu_id = input("Rich Menu ID:")
    if(not yes):yes = askyes()
    if(not yes):return False
    line_bot_api.delete_rich_menu(rich_menu_id)
    return True

def del_cancel_default_rich_menu(line_bot_api:LineBotApi, timeout=None, yes=False):
    if(not yes):yes = askyes()
    if(not yes):return False
    line_bot_api.cancel_default_rich_menu()
    return True

def info_get_default_rich_menu(line_bot_api:LineBotApi, timeout=None):
    rmid = line_bot_api.get_default_rich_menu()
    if(rmid):
        print(f"default rich menuid:{rmid}")
        return True
    return False

def doline(dbpm:DBPm, args):
    line_bot_api = LineBotApi(os.environ['LCAT'])
    if(args.target == 'rich_menu_create'):
        print("以預設值建立新的Rich Menu")
        r = init_default_rich_menu(line_bot_api=line_bot_api, yes=args.yes)
    elif(args.target == 'rich_menu_img_upload'):
        print("上傳Rich Menu 圖片")
        r = add_upload_rich_menu_img(line_bot_api=line_bot_api, yes=args.yes)
    elif(args.target == 'show_rich_menu_list'):
        print("顯示Rich Menu列表")
        r = info_get_rich_menu_list(line_bot_api=line_bot_api)
    elif(args.target == 'get_default_rich_menu'):
        print("顯示預設Rich Menu")
        r = info_get_default_rich_menu(line_bot_api=line_bot_api)
    elif(args.target == 'set_default_rich_menu'):
        print("設定預設的Rich Menu")
        r = add_set_default_rich_menu(line_bot_api = line_bot_api, yes=args.yes)
    elif(args.target == 'cancel_default_rich_menu'):
        print("取消預設的Rich Menu")
        r = del_cancel_default_rich_menu(line_bot_api=line_bot_api, yes=args.yes)
    elif(args.target == 'delete_rich_menu'):
        print("刪除Rich Menu")
        r = del_delete_rich_menu(line_bot_api=line_bot_api, yes=args.yes)
    if(r):print("成功")
    else:print("失敗")

def loadargs():
    parser = argparse.ArgumentParser()
    
    subparsers = parser.add_subparsers(title='資料庫控制', description='呼叫資料庫命令', dest='subparser_name')

    init = subparsers.add_parser('init')
    init.add_argument('target', choices=dblist, help='初始化資料庫目標')
    init.add_argument('-y', '--yes', action='store_true', help='確認執行')
    init.set_defaults(func = doinit)

    add = subparsers.add_parser('add')
    add.add_argument('target', choices=dblist, help='新增紀錄')
    add.add_argument('-y', '--yes', action='store_true', help='確認執行')
    add.set_defaults(func = doadd)

    line = subparsers.add_parser('line')
    line.add_argument('target', choices=LineApiList, help='Line API功能')
    line.add_argument('-y', '--yes', action='store_true', help='確認執行')
    line.set_defaults(func = doline)
    return parser.parse_args()

args = loadargs()
dbpm = DBPm()
print(args)
args.func(dbpm, args)
