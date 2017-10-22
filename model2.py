from datetime import datetime
from model import Model

class Model2(Model):

    def __init__(self, db, pair_id, fit_interval, granularity, initial_coin = 0, initial_fiat = 100, pct_high = 15, pct_low = 10):
        super().__init__(db, pair_id, fit_interval, granularity, initial_coin, initial_fiat, pct_high, pct_low)
        self.rate_bought = 0
        self.rate_sold = 0
        self.ts_buy = 0
        self.ts_sell = 0
        self.pct_high = pct_high
        self.ts_granularity = 0
        self.max_idle_time = 3600*24*20

    def buy(self, fiat, rate, ts):
        self.balance_coin += fiat / rate
        self.balance_fiat -= fiat
        self.rate_bought = rate
        self.ts_buy = ts
        self.ts_last = ts
        self.print_balance('b', rate)


    def sell(self, coin, rate, ts):
        self.balance_fiat += coin * rate
        self.balance_coin -= coin
        self.rate_sold = rate
        self.ts_sell = ts
        self.ts_last = ts
        self.print_balance('s', rate)

    def newpoint(self, ts, value):
        value = float(value)
        if self.start:
            self.buy(self.balance_fiat, value, ts)
            self.ts_last = ts
            self.start = False
            return
        if ts - self.ts_granularity < self.granularity:
            return
        self.ts_granularity = ts

        if value > (1 + self.pct_high / 100.0) * self.rate_bought and self.balance_coin > 0:
            self.sell(self.balance_coin, value, ts)
        elif value <= (1 - self.pct_low / 100.0) * self.rate_sold and self.balance_fiat > 0:
            self.buy(self.balance_fiat, value, ts)
        elif ts > self.ts_sell + self.max_idle_time and ts > self.ts_buy + self.max_idle_time:
            if self.ts_sell > self.ts_buy and self.balance_fiat > 0:
                self.buy(self.balance_fiat / 2.0,  value, ts)
            elif self.balance_coin > 0:
                self.sell(self.balance_coin / 2.0, value, ts)


