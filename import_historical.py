#!/usr/bin/python3
from datetime import datetime, timezone
from getopt import getopt
import json
import psycopg2
import sys, os
from time import time, sleep
import urllib, urllib.request

# 1383839436.659
# 1383839436 659595694

URL = 'https://api.kraken.com/0/public/Trades?pair=%s&since=%d'

def date2ts(s):
    return datetime.strptime(s, '%Y-%m-%d').replace(tzinfo=timezone.utc).timestamp()

def main():
    FROM = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
    TO = datetime.utcnow().replace(hour=23, minute=59, second=59, microsecond=59).timestamp()
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
            cur.execute('SELECT MAX(ts) FROM historical')
            FROM = cur.fetchone()[0]
        else:
            raise Exception("Unknown option: %s" % o)

    cur.execute('SELECT id, kname FROM pairs WHERE name=%s', (PAIR,))
    pair_id, KPAIR = cur.fetchone()

    ctime = FROM
    done = False
    while ctime < TO and not done:
        print(datetime.utcfromtimestamp(ctime))
        url = URL % (KPAIR, (ctime * 1000000000))
        with urllib.request.urlopen(url) as resp:
            kdata = resp.read().decode('latin1')
        data = json.loads(kdata)
        if data['error']:
            print(data['error'])
            if 'EService:Unavailable' in data['error']:
                sleep(2)
                continue
            raise Exception(repr(data['error']))
        cur.execute('DELETE FROM historical WHERE ts BETWEEN %s AND %s', (data['result'][KPAIR][0][2], data['result'][KPAIR][-1][2]))
        idata = [ cur.mogrify('(%s,%s,%s,%s,%s)', (pair_id, d[0], d[1], d[3], d[2])) for d in data['result'][KPAIR] ]
        cur.execute(b'INSERT INTO historical(pair_id, value, volume, op, ts) VALUES %s' % b','.join(idata))
        for d in data['result'][KPAIR]:
            if d[2] > ctime:
                ctime = d[2]
        if ctime > datetime.utcnow().timestamp()-10:
            done = True
        db.commit()



if __name__ == '__main__':
    main()

