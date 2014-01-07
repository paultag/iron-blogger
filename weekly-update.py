#!/usr/bin/python
import render
import os
import sys
import xmlrpclib
import subprocess
import datetime
import yaml

from config import *

dry_run = False

args = sys.argv[1:]
if args[0] == '-n':
    dry_run = True
    args = args[1:]

date = args[0]

with open('ledger', 'a') as f:
    f.write("\n")
    f.write(render.render_template('templates/ledger', date))

if not dry_run:
    subprocess.check_call(["git", "commit", "ledger",
                           "-m", "Update for %s" % (date,)])

debts = render.get_debts()
punt = []

with open('ledger', 'a') as f:
    f.write("\n")
    for (user, debt) in debts:
        if debt <= (FINE_SIZE * 6): continue
        punt.append(user)
        f.write("""\
%(date)s Punt
  Pool:Owed:%(user)s  -%(debt)s
  User:%(user)s
""" % {'user': user, 'debt': debt, 'date': date})


if not dry_run:
    text = render.render_template('templates/week.tmpl', date, punt=punt)
    # Let's write to meta/notes/{week}.md
    with open("meta/notes/{week}.md".format(week=date), 'w') as fd:
        fd.write(text)
    # right, then let's update current.md
    if os.path.exists("meta/notes/pages/current.md"):
        os.unlink("meta/notes/pages/current.md")
    os.symlink("meta/notes/{week}.md".format(week=date),
               "meta/notes/pages/current.md")

email = render.render_template('templates/email.txt', date, punt=punt)

if dry_run:
    print email
else:
    p = subprocess.Popen(['mutt', '-H', '/dev/stdin'],
                         stdin=subprocess.PIPE)
    p.communicate(email)

if punt:
    with open('bloggers.yml') as b:
        bloggers = yaml.safe_load(b)
    for p in punt:
        if 'end' not in bloggers[p]:
            bloggers[p]['end'] = datetime.date(*map(int, date.split("-")))
    with open('bloggers.yml','w') as b:
        yaml.safe_dump(bloggers, b)

    if not dry_run:
        subprocess.check_call(["git", "commit", "ledger", "bloggers.yml",
                               "-m", "Punts for %s" % (date,)])

# if it's a dry run, lets set the ledger back to the beginning state
if dry_run:
    subprocess.check_call(["git", "checkout", "ledger"])

    if punt:
        subprocess.check_call(["git", "checkout", "bloggers.yml"])
