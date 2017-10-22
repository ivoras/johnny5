from datetime import datetime
from model import Model

class Model2(Model):

    def __init__(self, db, pair_id, fit_interval, granularity, initial_coin = 0, initial_fiat = 100, pct_high = 10, pct_low = 5):
        super().__init__(db, pair_id, fit_interval, granularity)
        self.start = True
        self.balance_coin = initial_coin
        self.balance_fiat = initial_fiat
        self.rate_bought = 0
        self.rate_sold = 0
        self.ts_buy = 0
        self.ts_last = 0
        self.ts_sell = 0
        self.pct_high = pct_high
        self.pct_low = pct_low

    def buy(self, fiat, rate, ts):
        self.balance_coin += fiat / rate
        self.balance_fiat -= fiat
        self.rate_bought = rate
        self.ts_buy = ts
        self.ts_last = ts
        print('b', self.balance_coin, self.balance_fiat)


    def sell(self, coin, rate, ts):
        self.balance_fiat += coin * rate
        self.balance_coin -= coin
        self.rate_sold = rate
        self.ts_sell = ts
        self.ts_last = ts
        print('s', self.balance_coin, self.balance_fiat)

    def newpoint(self, ts, value):
        value = float(value)
        if self.start:
            self.buy(self.balance_fiat, value, ts)
            self.ts_last = ts
            self.start = False
            return
        if ts - self.ts_last < self.granularity:
            return
        if value > (1 + self.pct_high / 100) * self.rate_bought and self.balance_coin > 0:
            self.sell(self.balance_coin, value, ts)
        elif value <= (1 - self.pct_low / 100) * self.rate_sold and self.balance_fiat > 0:
            self.buy(self.balance_fiat, value, ts)

