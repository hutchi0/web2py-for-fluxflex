# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.title = request.application
response.subtitle = T('customize me!')

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Your Name <you@example.com>'
response.meta.description = 'a cool new app'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'
response.meta.copyright = 'Copyright 2011'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('Home'), False, URL('default','index'), [])
    ]

response.menu += [
    (T('Galleries'), False, URL('categories'), [])
    ]
response.menu += [
    (T('Biography'), False, URL('biography'), [])
    ]

response.menu += [
    (T('Contact'), False, URL('contact'), [])
    ]

if auth.user and auth.user.id<3:
    response.menu += [
    (T('edit images'), False, URL('edit_images'), [])
    ]

    response.menu += [
    (T('edit galleries'), False, URL('edit_galleries'), [])
    ]
    response.menu += [
    (T('edit personal'), False, URL('edit_personal'), [])
    ]


#########################################################################
## provide shortcuts for development. remove in production
#########################################################################
def _():
    ()

