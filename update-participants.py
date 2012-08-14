#!/usr/bin/python

import render
import os
import sys
import xmlrpclib
import subprocess

from config import *

try:
    subprocess.call(['stty', '-echo'])
    passwd = raw_input("Password for %s: " % (USER,))
    print
finally:
    subprocess.call(['stty', 'echo'])

x = xmlrpclib.ServerProxy(XMLRPC_ENDPOINT)
page = x.wp.getPage(BLOG_ID, PARTICIPANTS_PAGE_ID, USER, passwd)

text = render.render_template('templates/users.tmpl')
page['description'] = text

x.wp.editPage(BLOG_ID, PARTICIPANTS_PAGE_ID, USER, passwd, page, True)
