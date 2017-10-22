from datetime import datetime
from model import Model
from scipy.optimize import curve_fit
from numpy import polyfit, poly1d

def mfunc(x, a, b):
    return a + b * x

class Model1(Model):

    def calcpint(self, ts, n):
        cur = self.db.cursor()
        from_ts = ts - (self.fit_interval * n)
        #print(datetime.utcfromtimestamp(ts), datetime.utcfromtimestamp(from_ts))
        cur.execute('SELECT ts, value::float FROM historical WHERE pair_id=%s AND ts BETWEEN %s AND %s ORDER BY ts', (self.pair_id, from_ts, from_ts + self.fit_interval))
        x = []
        y = []
        old_x = None
        for p in cur:
            if old_x != None and p[0] - old_x < self.granularity: 
                continue
            else:
                old_x = p[0]
            x.append(p[0])
            y.append(p[1])
        if len(x) < 3:
            return None
        return polyfit(x, y, 2)


    def newpoint(self, ts, value):
        value = float(value)

        histp = [ self.calcpint(ts, 4), self.calcpint(ts, 3), self.calcpint(ts, 2), self.calcpint(ts, 1) ]
        if None in histp: return

        mp = [ c[0] for c in histp ]

        """
        if mp[0] > 0 and mp[1] > 0 and mp[2] > 0 and mp[3] > 0:
            what = Model.RISING
        elif mp[0] < 0 and mp[1] < 0 and mp[2] < 0 and mp[3] < 0:
            what = Model.FALLING
        elif mp[0] < 0 and mp[1] < 0 and mp[2] > 0 and mp[3] > 0:
            what = Model.START_RISING
        elif mp[0] > 0 and mp[1] > 0 and mp[2] < 0 and mp[3] < 0:
            what = Model.START_FALLING
        else:
            what = Model.UNKNOWN
        """
        pp = polyfit([ts-4*self.fit_interval, ts-3*self.fit_interval, ts-2*self.fit_interval, ts-1*self.fit_interval], mp, 1)[0]
        if pp > 0 and mp[0] > 0:
            what = Model.RISING
        elif pp < 0 and mp[0] < 0:
            what = Model.FALLING
        elif pp > 0 and mp[0] < 0:
            what = Model.START_RISING
        elif pp < 0 and mp[0] > 0:
            what = Model.START_FALLING
        else:
            what = Model.UNKNOWN

        #c = curve_fit(mfunc, x, y)
        p = poly1d(histp[3])
        print(ts, p(ts) - value, value, what)

