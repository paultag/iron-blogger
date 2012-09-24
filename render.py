#!/usr/bin/python
import yaml
from dateutil.parser import parse
import datetime
import dateutil.tz as tz
import sys
import os
import os.path
import subprocess
import re
from mako.template import Template

from config import *

def get_balance(acct):
    p = subprocess.Popen(BALANCE_CMD + [acct],
                         stdout=subprocess.PIPE)
    (out, _) = p.communicate()
    return float(re.sub(r'\s*(\d+)\s+.*', r'\1', out))

def get_debts():
    p = subprocess.Popen(DEBTS_CMD,
                         stdout=subprocess.PIPE)
    (out, _) = p.communicate()
    debts = []
    for line in out.split("\n"):
        if not line: continue
        (val, acct) = line.split()
        user = acct[len("Pool:Owed:"):]
        if not user: continue
        val = float(re.sub(r'(\D)?(\d+)$', r'\2', val))
        debts.append((user, val))
    return debts

def to_week_num(date):
    return (parse(date, default=START) - START).days / 7

def parse_skip(rec):
    spec = rec.get('skip', [])
    out = []
    for s in spec:
        if isinstance(s, list):
            out.append(map(to_week_num, s))
        else:
            out.append(to_week_num(s))
    return out

def should_skip(skips, week):
    for e in skips:
        if e == week:
            return True
        if isinstance(e, list) and e[0] <= week and e[1] > week:
            return True
    return False

def render_template(path, week=None, **kwargs):
    with open('out/report.yml') as r:
        report = yaml.safe_load(r)

    with open('bloggers.yml') as f:
        users = yaml.safe_load(f)
    if week:
        week = parse(week, default=START)
    else:
        week = START

    week = (week - START).days / 7
    week_start = START + (week * datetime.timedelta(7))
    week_end   = START + ((week + 1) * datetime.timedelta(7))

    good = []
    lame = []
    skip = []
    userlist = []
    punted = []

    class User(object):
        pass

    for (un, rec) in users.items():
        u = User()
        u.username = un
        u.links = rec['links']
        u.start = rec['start']
        u.end   = rec.get('end')
        u.skip  = parse_skip(rec)
        u.weeks = report.get(un, [])

        userlist.append(u)

        # create a subset of punted users
        if u.end:
            punted.append(u)

    def user_key(u):
        return (u.start, u.username)

    userlist.sort(key=user_key)
    punted.sort(key=user_key)

    for u in userlist:
        user_start = datetime.datetime(*(u.start.timetuple()[:6]))
        if u.end and datetime.datetime(*(u.end.timetuple()[:6])) <= week_start:
            continue
        
        if should_skip(u.skip, week):
            pass
        elif user_start > week_start:
            skip.append(u)
        elif len(u.weeks) <= week or not u.weeks[week]:
            lame.append(u)
        else:
            good.append(u)

    debts = get_debts()

    return Template(filename=path, input_encoding='utf-8',
                    output_encoding='utf-8',
                    default_filters=['decode.utf8']).render(
        week=week, week_start=week_start,week_end=week_end,
        good=good, lame=lame, skip=skip, userlist=userlist,
        pool=get_balance('Pool'), paid=get_balance('Pool:Paid'),
        debts=debts, punted=punted, currency=CURRENCY, fine=FINE_SIZE,
        **kwargs)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print >>sys.stderr, "Usage: %s TEMPLATE [WEEK]"
        sys.exit(1)

    template = sys.argv[1]
    week = None
    if len(sys.argv) > 2: week = sys.argv[2]
    print render_template(template, week)
