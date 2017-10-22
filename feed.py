class Feed:

    class NoMore(Exception):
        pass


class HistoricalFeed(Feed):

    def __init__(self, db, pair_id, start_ts = None, interval = None):
        self.db = db
        self.pair_id = pair_id
        self.cur = db.cursor()
        self.start_ts = start_ts
        self.interval = interval
        self.cts = start_ts

    def next(self):
        ts = self.cts + self.interval
        self.cur.execute('SELECT value FROM historical WHERE pair_id=%s AND ts >= %s ORDER BY ts LIMIT 1', (self.pair_id, ts,))
        self.cts = ts
        row = self.cur.fetchone()
        if not row:
            raise Feed.NoMore()
        return ts, row[0]


