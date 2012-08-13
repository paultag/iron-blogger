#!/usr/bin/python
## -*- coding: utf-8 -*-

import os.path
import datetime
import subprocess

HERE  = os.path.dirname(__file__)
START = datetime.datetime(2011, 10, 24, 6)

XMLRPC_ENDPOINT = 'http://iron-blogger.mako.cc/xmlrpc.php'
USER            = 'mako'
BLOG_ID         = 1
PARTICIPANTS_PAGE_ID         = 12

FINE_SIZE = 5
CURRENCY = "$"

# check the version of ledger to find out which commands to use
if subprocess.check_output(['ledger', '--version'])[7] == 3:
    BALANCE_CMD = ['ledger', '-f', os.path.join(HERE,'ledger'),
                   '--no-color', '-n', 'balance']

    DEBTS_CMD = ['ledger', '-f', os.path.join(HERE, 'ledger'),
                 '--flat', '--no-total', '--no-color',
                 'balance', 'Pool:Owed:']

else:
    BALANCE_CMD = ['ledger', '-f', os.path.join(HERE, 'ledger'),
                   '-n', 'balance']
    DEBTS_CMD = ['ledger', '-f', os.path.join(HERE, 'ledger'),
                 '-n', 'balance', 'Pool:Owed:']
    
