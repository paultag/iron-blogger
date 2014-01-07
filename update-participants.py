#!/usr/bin/python

import render

text = render.render_template('templates/users.tmpl')
open('meta/notes/pages/participants.md', 'w').write(text)
