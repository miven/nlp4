'''
把这个代码贴到  https://www.fmz.com/m/add-strategy

这里面直接跑就行了.


注意一定要选好平台和产品
平台用OKCoin国际   产品是BTC_USD  选好后,点红色加号.


假设 1  1000 现金     1000price/bit
    1.5   750       500 price/bit         (因为跌倒500块一个了,所以我们拿250块钱去买,这样我们现金750==1.5*500)
   1.125   1125         1000/bit       (长回了1000块一个,我们就卖掉一些.)



假设 1  1000 现金     1000price/bit  (起始资金2000快)
    1.5   750       500 price/bit         (因为跌倒500块一个了,所以我们拿250块钱去买,这样我们现金750==1.5*500)
   2.625   525         200/bit       (长继续跌倒200块一个)  而我们如果一直没有操作的话我们现在价值1200而不是现在的1050



# 结论:
1. 收益来源于,来回波动
2.风险来源于, 一直下跌.


# 一般来说 金额变动在手续费4倍左右比较合理.  不然买卖比较困难.性价比太低.
# 如果市场活跃, 那么1.5倍-2倍也是可以. 因为有人接盘.
# 市场不活跃的时候 8被,10倍,50倍都是可以的.







这个是半仓策略: 很简单,就是如果涨了我们就卖到半仓.如果跌了我们就买入到半仓.
这种策略长期而言是会赚的(如果是上下波动的情况),短期而言是不一定会赚.
'''
##
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


## %%


'''
这个类,就是核心策略类,每一次新的策略,就是修改这个class即可.
'''
class juncang_class():
    def __init__(self, mid_class,rate,rate2):
        self.buytorate=rate # 这个比例表示我买之后要把仓里面总金额的多少比例干成股票
        self.selltorate=rate2# 表示我卖之后要把股票干成多少比例.
        self.jys = mid_class
        self.last_time = time.time()
        self.last_trade_price = self.jys.last


# 获取所有需要的信息.吧他们邪道对象的属性道中.
    def make_need_account_info(self):
        self.jys.refreash_data()
        self.B = self.jys.Amount     # 账户的股票的数量
        self.money = self.jys.Balance  # 账户的资金数量
        now_price = self.jys.last  # 最新的价格   我们的策略就是用这3个来

        self.total_money = self.B * now_price + self.money
        self.gupiao_money = self.total_money *self.buytorate
        self.need_buy = (self.total_money *self.buytorate - self.B * now_price) / now_price #其实就是把总金额的一般换成股票
        # 需要买进的数量  ,当然只有价格比之前下降了,我们这个才是正数.否则是一个负数.

# 卖掉x s.t.     ( self.B-x)*now_price+self.money

        self.need_sell = (self.B*now_price-self.selltorate*self.total_money) / now_price
        # 需要卖掉的股票的数量.

        '''
        首先我们要知道,为什么这种策略会, 任何时间都有钱来买和卖.卖是肯定可以的.但是为什么一直有钱买?
        因为每一次我们都剩余了半仓的钱.所以最坏的情况是:
        股票一直下降,我们需要一直买,这样我们的钱会越来越少,但是始终会让我们有资金去买.
        所以类似的我们可以写出2/3仓.这种策略.或者百分之多少都行.只要小于1就行.
        '''

    def do_juncang(self):
        # 这个参数表示跳跃多大的时候,才开始交易,如果小了就会尽量抓取每一个谢姐
        # 如果大了就会尽可能抓取峰值和低值.但是风险也高,          所以需要做实验微调
        # 因为市场一般是0.01手续费,所以这里面一般从0.03以上开始设置比较合理.
        quanzhong=0.01
        #
        if self.need_buy > quanzhong:# 因为交易所手续费是千分之一.
            self.jys.create_order('buy', self.jys.low, self.need_buy)
        elif self.need_sell > quanzhong:
            self.jys.create_order('sell', self.jys.high, self.need_sell)

    def if_need_trade(self, condition, prama):
        #其实这个时间间隔触发器没屁用,我们不会用
        if condition == 'time':


            if time.time() - self.last_time > prama:
                self.do_juncang()
                self.last_time = time.time()

        # 我们只会用这个价格,当当前价格,比我们股票上次交易的价格, 变动超过 param就会触发.
        if condition == 'price':
            if abs(self.jys.last - self.last_trade_price) / self.last_trade_price > prama:
                self.do_juncang()
                self.last_trade_price = self.jys.last


# %%
# 这个也不用动.  网页上的代码会自动调用这个main
def main():
    test_mid = mid_class(exchange)
    Log(test_mid.refreash_data())
    # 参数表示 我买就买到0.8 仓,我卖就卖到0.2仓
    # 第一个数字越大表示越波动.越小越保守, 第二个数字一样.
    test_juncang = juncang_class(test_mid,0.4,0.2)

    while (True):

            Sleep(60)
            test_juncang.make_need_account_info()
            ## 这个参数表示跳跃多大的时候,才开始交易,如果小了就会尽量抓取每一个谢姐, 跟上面
            #那个参数作用一样, 都是调节参数让他尽可能高卖低买. 具体参数需要调.根据回调来调.
            # p越大表示交易量越小.越疯狂买卖.越激进.  p越大越容易抓到峰值和低值.更容易暴利!!!!!!!!!
            p=0.05
            test_juncang.if_need_trade('price', p)


