from datetime import datetime

class Model:

    RISING = 2000
    START_RISING = 1000
    UNKNOWN = 0
    START_FALLING = -1000
    FALLING = -2000

    def __init__(self, db, pair_id, fit_interval, granularity, initial_coin = 0, initial_fiat = 100, pct_high = 10, pct_low = 5):
        self.db = db
        self.pair_id = pair_id
        self.fit_interval = fit_interval
        self.granularity = granularity
        self.balance_coin = initial_coin
        self.balance_fiat = initial_fiat
        self.pct_high = pct_high
        self.pct_low = pct_low
        self.ts_last = 0
        self.start = True

    def newpoint(self, ts, value):
        pass

    def print_balance(self, mark=' ', rate=0):
        ts = datetime.utcfromtimestamp(self.ts_last)
        if rate == 0:
            print('%s %s %0.8f %0.2f' % (ts, mark, self.balance_coin, self.balance_fiat))
        else:
            print('%s %s %0.8f %0.2f [%0.2f]' % (ts, mark, self.balance_coin, self.balance_fiat, self.total_balance(rate)))

    def total_balance(self, rate):
        return self.balance_fiat + self.balance_coin * rate

