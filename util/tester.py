import argparse
from dbPm import DBPm

dblist = ['cart_items', 'coupon', 'customers', 'messaging_log', 'orders', 'payment_log', 'product_category', 'products', 'shopping_cart']

def askyes():
    val = input("Confirm to Do(Y/N):").lower()
    if(val == 'y' or val == 'yes'):return True
    else:return False

def init_product_category(dbpm:DBPm, yes=False):
    if(not yes):yes = askyes
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
    return True

def doinit(dbpm:DBPm, args):
    if(args.target == 'product_category'):
        print("插入product_category測試資料")
        init_product_category(dbpm=dbpm, yes=args.yes)

def loadargs():
    parser = argparse.ArgumentParser()
    
    subparsers = parser.add_subparsers(title='資料庫控制', description='呼叫資料庫命令', dest='subparser_name')
    init = subparsers.add_parser('init')
    init.add_argument('target', choices=dblist, help='初始化資料庫目標')
    init.add_argument('-y', '--yes', action='store_true', help='確認執行')
    init.set_defaults(func = doinit)

    add = subparsers.add_parser('add')
    add.add_argument('target', choices=dblist, help='新增紀錄')
    return parser.parse_args()

args = loadargs()
dbpm = DBPm()
print(args)
args.func(dbpm, args)
