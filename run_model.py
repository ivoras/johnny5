#!/usr/bin/python3
from datetime import datetime, timezone
from getopt import getopt
import json
import psycopg2
import sys, os

from feed import Feed, HistoricalFeed
from model1 import Model1
from model2 import Model2

def date2ts(s):
    return datetime.strptime(s, '%Y-%m-%d').replace(tzinfo=timezone.utc).timestamp()

def main():
    FROM = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
    TO = datetime.utcnow().timestamp()
    PAIR = 'BTCEUR'

    db = psycopg2.connect('dbname=johnny5 user=johnny5')
    cur = db.cursor()

    opts, args = getopt(sys.argv[1:], 'f:lp:t:')

    for o, a in opts:
        if o == '-f':
            FROM = date2ts(a)
        elif o == '-p':
            PAIR = a
        elif o == '-t':
            TO = date2ts(a)
        elif o == '-l':
            cur.execute('SELECT MIN(ts) FROM historical')
            FROM = cur.fetchone()[0]
        else:
            raise Exception("Unknown option: %s" % o)

    cur.execute('SELECT id, kname FROM pairs WHERE name=%s', (PAIR,))
    pair_id, KPAIR = cur.fetchone()

    f = HistoricalFeed(db, pair_id, FROM, 3600)
    m = Model2(db, pair_id, 6*3600, 1*3600)

    while True:
        try:
            ts, value = f.next()
        except Feed.NoMore:
            break
        if ts >= TO: break
        action = m.newpoint(ts, value)
        #print(action)

if __name__ == '__main__':
    main()

