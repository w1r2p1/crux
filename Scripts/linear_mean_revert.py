import numpy as np
import matplotlib.pyplot as plt
import math

file = open("../data/polo_LTC_USD1hour.csv")
lines = file.readlines()
file.close()

price = [float(l.split(',')[1]) for l in lines]
price = price[11000:]

pl = []
apl = []
trade = []

FRICTION = 0.005
MA_LAG = 48
ma = [0 if i < MA_LAG-1 else np.average(price[i-MA_LAG+1:i+1]) for i in range(len(price))]
mstd = [0 if i < MA_LAG-1 else np.std(price[i-MA_LAG+1:i+1]) for i in range(len(price))]

usd = 100
btc = 100

start_value = usd + btc * price[MA_LAG-1]

walusd = []
walbtc = []

np.seterr(all='raise')

for i in range(MA_LAG-1, len(price)):
	mstd[i] = max(mstd[i], 0.001)

	z = -(price[i] - ma[i]) / mstd[i]

	val = usd + btc * price[i]

	if z > 0: #buy
		new_usd = val / (2+z)
		diff = usd - new_usd
		trade.append(0 if diff > 0 else 1)
		usd = new_usd
		btc += (diff / price[i]) * (1 - FRICTION)
	else:	#sell
		new_btc = val / (2-z)
		diff = btc * price[i] - new_btc
		trade.append(0 if diff < 0 else 1)
		btc = new_btc / price[i]
		usd += diff * (1 -  FRICTION)

	pl.append((usd + btc * price[i]) / start_value)
	apl.append(price[i]/price[MA_LAG-1])
	walusd.append(usd)
	walbtc.append(btc)


val = usd + btc * price[-1]
print ("Total: {}".format(val))
print ("USD: {}".format(usd))
print ("BTC: {}".format(btc))
print ("Final PL: {}".format(val / start_value))
print ("Asset PL: {}".format(price[-1] / price[MA_LAG-1]))

plt.plot(pl, label='Strategy P/L MA:{}'.format(MA_LAG))
plt.plot(apl, label='Asset P/L')
# plt.plot(walusd)
# plt.plot(walbtc)

# trade = np.array(trade)
# price = np.array(price[MA_LAG-1:])
# buys = np.where(trade == 0)[0]
# sells = np.where(trade == 1)[0]

# plt.plot(price)
# plt.plot(ma[MA_LAG-1:])
# plt.scatter(buys, price[buys], c='green')
# plt.scatter(sells, price[sells], c='red')

plt.legend(loc='upper left')
plt.show()