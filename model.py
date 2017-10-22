
class Model:

    RISING = 2000
    START_RISING = 1000
    UNKNOWN = 0
    START_FALLING = -1000
    FALLING = -2000

    def __init__(self, db, pair_id, fit_interval, granularity):
        self.db = db
        self.pair_id = pair_id
        self.fit_interval = fit_interval
        self.granularity = granularity

    def newpoint(self, ts, value):
        pass

