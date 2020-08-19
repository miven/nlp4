# %% md  https://www.fmz.com/m/add-strategy
# 平台: 火币  , btc_usdt,
# 做市策略
### 1、对敲做量    这个脚本就是做这个对敲的策略. 后面的策略会在其他.py里面写.  说白了就是刷单.
### 2、盘口高频吃利润
### 3、缓步先买后卖抬高品种价格
### 4、缓步先卖后买拉低品种价格

# %%

'''
下面实现的是第一种作市策略,就是简单的对敲.自己卖然后自己买. 用同样的价格反复买卖.来激活市场.

'''
class mid_class():
    def __init__(self, this_exchange):
        '''
        初始化数据填充交易所的信息，首次获取价格，首次获取account信息
        设定好密钥……

        Args:
            this_exchange: FMZ的交易所结构

        '''
        self.init_timestamp = time.time()
        self.exchange = this_exchange
        self.name = self.exchange.GetName()
        self.jyd = self.exchange.GetCurrency()

    def get_account(self):
        '''
        获取账户信息

        Returns:
            获取信息成功返回True，获取信息失败返回False
        '''
        self.Balance = '---'
        self.Amount = '---'
        self.FrozenBalance = '---'
        self.FrozenStocks = '---'

        try:
            self.account = self.exchange.GetAccount()

            self.Balance = self.account['Balance']
            self.Amount = self.account['Stocks']
            self.FrozenBalance = self.account['FrozenBalance']
            self.FrozenStocks = self.account['FrozenStocks']
            return True
        except:
            return False

    def get_ticker(self):
        '''
        获取市价信息          一个ticker叫做一次交易.这个函数获取当前市场价格表.

        Returns:
            获取信息成功返回True，获取信息失败返回False
        '''
        self.high = '---'
        self.low = '---'
        self.Sell = '---'
        self.Buy = '---'
        self.last = '---'
        self.Volume = '---'

        try:
            self.ticker = self.exchange.GetTicker()

            self.high = self.ticker['High']
            self.low = self.ticker['Low']
            self.Sell = self.ticker['Sell']
            self.Buy = self.ticker['Buy']
            self.last = self.ticker['Last']
            self.Volume = self.ticker['Volume']
            return True
        except:
            return False

    def get_depth(self):
        '''
        获取深度信息

        Returns:
            获取信息成功返回True，获取信息失败返回False
        '''
        self.Ask = '---'
        self.Bids = '---'

        try:
            self.Depth = self.exchange.GetDepth()
            self.Ask = self.Depth['Asks']
            self.Bids = self.Depth['Bids']
            return True
        except:
            return False

    def get_ohlc_data(self, period=PERIOD_M5): # PERIOD_M5 表示间隔5分钟一次作为数据中的间隔.
        '''
        获取K线信息

        Args:
            period: K线周期，PERIOD_M1 指1分钟, PERIOD_M5 指5分钟, PERIOD_M15 指15分钟,
            PERIOD_M30 指30分钟, PERIOD_H1 指1小时, PERIOD_D1 指一天。
        '''
        self.ohlc_data = exchange.GetRecords(period)

    def create_order(self, order_type, price, amount):
        '''
        post一个挂单信息

        Args:
            order_type：挂单类型，'buy'指挂买单，'sell'指挂卖单
            price：挂单价格
            amount:挂单数量

        Returns:
            挂单Id号，可用以取消挂单
        '''
        if order_type == 'buy':
            try:
                order_id = self.exchange.Buy(price, amount)
            except:
                return False

        elif order_type == 'sell':
            try:
                order_id = self.exchange.Sell(price, amount)
            except:
                return False

        return order_id

    def get_orders(self):
        self.undo_ordes = self.exchange.GetOrders()
        return self.undo_ordes

    def cancel_order(self, order_id):
        '''
        取消一个挂单信息

        Args:
            order_id：希望取消的挂单ID号

        Returns:
            取消挂单成功返回True，取消挂单失败返回False
        '''
        return self.exchange.CancelOrder(order_id)

    def refreash_data(self):
        '''
        刷新信息

        Returns:
            刷新信息成功返回 'refreash_data_finish!' 否则返回相应刷新失败的信息提示
        '''

        if not self.get_account():
            return 'false_get_account'

        if not self.get_ticker():
            return 'false_get_ticker'
        if not self.get_depth():
            return 'false_get_depth'
        try:
            self.get_ohlc_data()
        except:
            return 'false_get_K_line_info'

        return 'refreash_data_finish!'


# %%

class zuoshi():
    # 所谓做式,就是自己卖,自己买.来影响市场. 吸引客户进来.然后割他们韭菜.
    def __init__(self, mid_class, amount_N, price_N):
        self.jys = mid_class
        self.done_amount = 0
        self.init_time = time.time()
        self.last_time = time.time()
        self.amount_N = amount_N  # 这2个变量表示精度.
        self.price_N = price_N

    def trade_duiqiao(self, trade_dict):


# 这里面也就是核心逻辑,也就是先买再卖. 买卖的价格都是一样的.所以就是刷单!!!!!!!!!!!!!!!!!!!!!
        self.jys.create_order('buy', trade_dict['price'], trade_dict['amount'])
        self.jys.create_order('sell', trade_dict['price'], trade_dict['amount'])
        self.done_amount += trade_dict['amount']
        self.last_time = time.time()

    def make_duiqiao_trade_dict(self, set_amount, every_time_amount):
        self.jys.refreash_data()

        trade_price = (self.jys.Sell + self.jys.Buy) / 2
        trade_price = round(trade_price, self.price_N)
        if trade_price > self.jys.Buy and trade_price < self.jys.Sell:
            self.B = self.jys.Amount  # 账户中比特币的舒朗.
            self.money = self.jys.Balance   # 账户中的钱
            self.can_buy_B = self.money / trade_price   # 把剩余的钱全买成股票
            do_trade = self.B > every_time_amount  # every_time_amount  表示每一次买的股票数量.
            do_trade = do_trade and self.can_buy_B > every_time_amount  # 因为一定要保证卖完之后还能再买回来,所以需要每次都检测交易的数量,这次服务可以有足够的股票和金钱来支撑.
            trade_dict = {'do_trade': do_trade,
                          'price': trade_price,
                          'amount': every_time_amount}
            return trade_dict


# 取消全部订单.
    def deal_with_frozen(self): # 把还没有生效的订单都取消了.
        undo_orders = self.jys.get_orders()
        if len(undo_orders) > 0:
            for i in undo_orders:
                self.jys.cancel_order(i['Id'])


# %%

def main():
    '''
    先设置超级参数.

    :return:
    '''
    Set_amount_N = 4
    Set_price_N = 4
    set_amount = 10
    every_time_amount = 0.1

    test_mid = mid_class(exchange)
    Log(test_mid.refreash_data())
    test_duiqiao = zuoshi(test_mid, Set_amount_N, Set_price_N)

    while (test_duiqiao.done_amount < set_amount):
        test_duiqiao.deal_with_frozen()  #先清空没用的交易, 然后下面开启新的交易.
        Sleep(1000)
        trade_dict = test_duiqiao.make_duiqiao_trade_dict(set_amount, every_time_amount)
        if trade_dict['do_trade']:
            test_duiqiao.trade_duiqiao(trade_dict)

    Log(test_duiqiao.done_amount)
    Log(test_duiqiao.B)
