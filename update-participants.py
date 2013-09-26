#!/usr/bin/python

import render

text = render.render_template('templates/users.tmpl')
open('out/participants.html', 'w').write(text)
