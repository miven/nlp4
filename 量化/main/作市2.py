# %% md
         # 作市策略第二种: 盘口高频.
### 1、写盘口高频策略
### 2、把对敲与盘口高频整合到一起

# %% md

### 盘口高频为何能有盈利空间
# - 1、市场上有人急着买，有人急着卖，急着买的买的和急着卖的差价就可以被你吃到
# - 2、市场存在微小的价格波动，类似于网格吃波动可以吃到利润


# %%

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
        获取市价信息

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

    def get_ohlc_data(self, period=PERIOD_M5):
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
'''
下面开始这个盘口高频的代码!!!!!!!!!!!!!!!
'''
# 现在这个就是盘口高频.
class zuoshi():
    def __init__(self, mid_class, amount_N, price_N):
        self.jys = mid_class
        self.done_amount = {'pan_kou': 0, 'dui_qiao': 0}
        self.init_time = time.time()
        self.last_time = time.time()
        self.amount_N = amount_N   # 数量的小数位精度
        self.price_N = price_N # 价格的小数位精度 一般取4
        self.wait_time = 60

        self.traded_pair = {'pan_kou': [], 'dui_qiao': []}
        self.undo_state = []
        self.had_gua_times = 0

    def refreash_data(self):

        self.jys.refreash_data()
        self.B = self.jys.Amount
        self.money = self.jys.Balance
        self.can_buy_B = self.money / self.jys.Buy
        self.mid_price = (self.jys.Sell + self.jys.Buy) / 2

        return

    def make_trade_by_dict(self, trade_dicts):
        for trade_dict in trade_dicts:
            if trade_dict['do_trade']:
                buy_id = self.jys.create_order('buy', trade_dict['buy_price'], trade_dict['amount'])
                sell_id = self.jys.create_order('sell', trade_dict['sell_price'], trade_dict['amount'])

                if trade_dict['buy_price'] == trade_dict['sell_price']: # 对敲就是不赚钱,
                    self.done_amount['dui_qiao'] += trade_dict['amount']
                    self.traded_pair['dui_qiao'].append({'buy_id': buy_id, 'sell_id': sell_id, 'init_time': time.time(),
                                                         'amount': trade_dict['amount']})
                else: # 盘口高频就是赚一点差价.

                    self.traded_pair['pan_kou'].append({'buy_id': buy_id, 'sell_id': sell_id, 'init_time': time.time(),
                                                        'amount': trade_dict['amount']})

                self.last_time = time.time()

    def make_duiqiao_trade_dict(self, set_amount, every_time_amount):

        trade_price = self.mid_price
        trade_price = round(trade_price, self.price_N)

        if trade_price > self.jys.Buy and trade_price < self.jys.Sell:
            do_trade = self.B > every_time_amount
            do_trade = do_trade and self.can_buy_B > every_time_amount
            trade_dict = {'do_trade': do_trade,
                          'buy_price': trade_price,
                          'sell_price': trade_price,
                          'amount': every_time_amount}

            return [trade_dict]

    def deal_with_frozen(self):
        undo_orders = self.jys.get_orders()
        if len(undo_orders) > 0:
            for i in undo_orders:
                self.jys.cancel_order(i['Id'])

    def make_pankou_dict(self, price_range, min_price_len, every_time_amount):
        mid_price = self.mid_price

        price_alpha = price_range - self.had_gua_times * min_price_len
        do_dict = price_alpha > 0
        if do_dict:

            buy_price = mid_price - price_alpha
            buy_price = round(buy_price, self.price_N)
            can_buy_B = self.money / buy_price

            sell_price = mid_price + price_alpha
            sell_price = round(sell_price, self.price_N)

            do_dict = do_dict and self.B > every_time_amount
            do_dict = do_dict and can_buy_B > every_time_amount

            amount = every_time_amount

            trade_dict = {'do_trade': do_dict,
                          'buy_price': buy_price,
                          'sell_price': sell_price,
                          'amount': every_time_amount}
            return [trade_dict]
        else:
            self.had_gua_times = 0

    def check_if_traded(self, now_times):
        for traded_id in self.traded_pair['pan_kou']:
            try:
                this_buy_state = self.jys.exchange.GetOrder(traded_id['buy_id'])
            except:
                self.jys.cancel_order(traded_id['sell_id'])
                self.traded_pair['pan_kou'].remove(traded_id)
            try:
                this_sell_state = self.jys.exchange.GetOrder(traded_id['sell_id'])
            except:
                self.jys.cancel_order(traded_id['buy_id'])
                self.traded_pair['pan_kou'].remove(traded_id)

            if {this_sell_state['Status'], this_buy_state['Status']} == {0, 0}: # 交易都失败了
                if now_times % 50 == 0:
                    Log(this_buy_state['Status'], this_sell_state['Status'], now_times % 50)
                    #                 if ( time.time() - traded_id['init_time'] )/1000/60 > self.wait_time:
                    self.jys.cancel_order(traded_id['buy_id'])
                    self.jys.cancel_order(traded_id['sell_id'])
                    self.had_gua_times += 0
                    self.traded_pair['pan_kou'].remove(traded_id)

            elif {this_sell_state['Status'], this_buy_state['Status']} == {1, 0}:   # {} 表示set
                if now_times % 50 == 0:
                    Log(this_buy_state['Status'], this_sell_state['Status'], now_times % 50)
                    #                 if ( time.time() - traded_id['init_time'] )/1000/60 > self.wait_time:
                    if this_buy_state['Status'] == 'ORDER_STATE_PENDING': # 哪个挂起就表示哪个没有成功还在继续中.
                        self.jys.cancel_order(traded_id['buy_id'])
                        self.undo_state.append(['buy', this_buy_state['Status']])
                        self.traded_pair['pan_kou'].remove(self.traded_id)
                    elif this_sell_state['Status'] == 'ORDER_STATE_PENDING':
                        self.jys.cancel_order(traded_id['sell_id'])
                        self.undo_state.append(['sell', this_sell_state['Status']])
                        self.traded_pair['pan_kou'].remove(self.traded_id)

            elif {this_sell_state['Status'], this_buy_state['Status']} == {1, 1}:
                Log(this_buy_state['Status'], this_sell_state['Status'], traded_id['amount'])
                self.done_amount['pan_kou'] += traded_id['amount']
                self.traded_pair['pan_kou'].remove(traded_id)
            else:
                Log(this_buy_state, this_sell_state)
                Log('2id:', this_buy_state['Status'], this_sell_state['Status'])
                Log(traded_id)


# %%

def main():
    times = 0

    Set_amount_N = 4
    Set_price_N = 4
    set_amount = 10

    price_range = 50
    min_price_len = 1
    every_time_amount = 0.01

    test_mid = mid_class(exchange)
    Log(test_mid.refreash_data())
    test_zuoshi = zuoshi(test_mid, Set_amount_N, Set_price_N)

    while (test_zuoshi.done_amount['pan_kou'] < set_amount):

        test_zuoshi.check_if_traded(times)
        Sleep(1000)
        test_zuoshi.refreash_data()

        if len(test_zuoshi.traded_pair['pan_kou']) < 1:
            trade_dicts = test_zuoshi.make_pankou_dict(price_range, min_price_len, every_time_amount)

        test_zuoshi.make_trade_by_dict(trade_dicts)
        Log(test_zuoshi.done_amount['pan_kou'])

        times += 1

    Log(test_zuoshi.B, test_zuoshi.can_buy_B)

