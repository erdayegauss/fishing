
import requests
# Define the risk taste, long: 0; short: 1; neutral: others. We devide the 3% between long and short position. 


# The target asset better be the low liqudity assets, the slipperage is larger
# X10: XRP, SAND, SHIB  
# X5:  XLM, MINA
# X3:  ONT, DYDX


asset="XRP"


# The target is the sell & buy difference, if 3%, with 10x leverage and transaction fee, the return could be 15%
# I would prefer to have a target of 0.01 or 0.02, with the return respectively 5% and 10%.
# Let's make it easy for everyday and better belive the compound power. 
# Less is more, slow is fast, we are always too smart to make it long run.
target=0.01

# The bias is the confidence of long position, if bias=0, we short imediately; if bias=1, we long imediately
bias=0.5



# Create a session and set proxy information (if required)
session = requests.session()
session.proxies = {
   'http': 'http://127.0.0.1:10900',
   'https': 'http://127.0.0.1:10900',
}


# session.auth = ("XXXXX", "YYYYY")

##margin account balance
account = session.get('https://api.hitbtc.com/api/3/margin/account')
balance = float(account.json()[1]["currencies"][0]['margin_balance'])


#### the current price
priceH = session.get('https://api.hitbtc.com/api/3/public/price/history?from='+asset+'&to=USDT')
priceR = session.get('https://api.hitbtc.com/api/3/public/price/rate?from='+asset+'&to=USDT')
price = float(priceR.json()[asset]['price'])

#### set buy and sell price based on current price. 
#### actually too much to be true
SellPrice=price*(1+bias*target)
BuyPrice=price*((1-(1-bias)*target))

print("The price and confidence are: ", price,bias)
print("The sell and buy prices are: ", SellPrice,BuyPrice)



# The quantity
quantity = int(balance*10*0.96/(2*price))
print("Sell and Buy simultaneously at size:", quantity)

SellOrderData = {'symbol':asset+'USDT', 'side': 'sell', 'time_in_force': 'Day', 'quantity': quantity, 'price': SellPrice}
# sell = session.post('https://api.hitbtc.com/api/3/margin/order', data = SellOrderData)

BuyOrderData = {'symbol':asset+'USDT', 'side': 'buy', 'time_in_force': 'Day', 'quantity': quantity, 'price': BuyPrice}
# buy = session.post('https://api.hitbtc.com/api/3/margin/order', data = BuyOrderData)






print(SellOrderData)
print(BuyOrderData)
