'''
使用撮合库包

'''



from lightmatchingengine.lightmatchingengine import LightMatchingEngine, Side

lme = LightMatchingEngine()

# (机构, 价格, 数量, 买or卖)
# order, trades = lme.add_order("EUR/USD", 1.10, 1000, Side.BUY)

buy_order, trades = lme.add_order("EUR/USD", 1.10, 1000, Side.BUY)
print("Number of trades = %d" % len(trades))                # Number of trades = 0
print("Buy order quantity = %d" % buy_order.qty)            # Buy order quantity = 1000
print("Buy order filled = %d" % buy_order.cum_qty)          # Buy order filled = 0
print("Buy order leaves = %d" % buy_order.leaves_qty)       # Buy order leaves = 1000


print('-------------------------')
sell_order, trades = lme.add_order("EUR/USD", 1.10, 1000, Side.SELL)
print("Number of trades = %d" % len(trades))                # Number of trades = 2
print("Buy order quantity = %d" % buy_order.qty)            # Buy order quantity = 1000
print("Buy order filled = %d" % buy_order.cum_qty)          # Buy order filled = 1000
print("Buy order leaves = %d" % buy_order.leaves_qty)       # Buy order leaves = 0


print('-------------------------')
print("Trade price = %.2f" % trades[0].trade_price)         # Trade price = 1.10
print("Trade quantity = %d" % trades[0].trade_qty)          # Trade quantity = 1000
print("Trade side = %d" % trades[0].trade_side)             # Trade side = 2






