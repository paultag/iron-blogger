#!/usr/bin/python
import yaml

f = open('bloggers.yml')
users = yaml.safe_load(f)

class User(object):
    pass

for (un, rec) in users.items():
    u = User()
    u.username = un
    u.end   = rec.get('end')
    
    if u.end:
        print "%s (punted: %s)" % (u.username, u.end)


