# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

if not request.env.web2py_runtime_gae:     
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite') 
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore') 
    ## store sessions and tickets there
    session.connect(request, response, db = db) 
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db, hmac_key=Auth.get_or_create_key()) 
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables() 

## configure email
mail=auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth,filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

db=SQLDB("sqlite://db.db")

from plugin_ckeditor import CKEditor 
ckeditor = CKEditor(db) 
ckeditor.define_tables() 




db.define_table('home',
                Field('image','upload'),
                Field('description', length=2096),
                Field('biography', length=2096))


db.define_table('personal',
                Field('first_name'),
                Field('surname'),
                Field('image','upload'),
                Field('description', 'text',length=2096),
                Field('biography', 'text',length=2096),
                Field('email'))

db.personal.biography.widget=ckeditor.widget
db.personal.description.widget=ckeditor.widget

db.personal.image.represent=lambda image,row: A(IMG(_src=URL('download',args=image),_height="120"),_href=URL('show_image',args=row.id, vars=request.vars))
db.personal.description.represent=lambda d,r:XML(d)
db.personal.biography.represent=lambda b,r:XML(b)
def idx(id):
    return A(IMG(_src=URL('download',args=db(db.image.show==id).select().first().thumb),_height="120"),_href=URL('category',args=id, vars=request.vars))


db.define_table('show',
  SQLField('name'))
db.show.name.requires=[IS_NOT_EMPTY(),IS_NOT_IN_DB(db,db.show.name)]
#db.show.id.represent=lambda id,row: A(IMG(_src=URL('download',args=db().select(db.image.show==id).first().file),_height="120"),_href=URL('show_image',args=row.id, vars=request.vars))
db.show.id.represent=lambda id, row:idx(id)
db.show.id.label=' '
db.show.name.label='Gallery'

db.define_table('image',
  Field('show',db.show),
  Field('title'),
  Field('size'),
  Field('media'),
  Field('price'),
  Field('file','upload'),
  Field('thumb','upload',writable=False))

def no_none(x):
    print x, "HH"
    if x==None:
        return " "
    else:
        return x
  
def thumbnail(infile):
    import os, sys
    from PIL import Image

    size = 128, 128

    outfile = os.path.splitext(infile)[0] + "tn"
    im = Image.open(infile)
    im.thumbnail(size)
    im.save(outfile, "JPEG")
    return outfile+".jpg"


class RESIZE(object): 
    def __init__(self,nx=160,ny=80,error_message='niepoprawny plik'): 
        (self.nx,self.ny,self.error_message)=(nx,ny,error_message) 
    def __call__(self,value):
        if isinstance(value, str) and len(value)==0: 
            return (value,None) 
        from PIL import Image 
        import cStringIO 
        try: 
            img = Image.open(value.file) 
            img.thumbnail((self.nx,self.ny), Image.ANTIALIAS) 
            s = cStringIO.StringIO() 
            img.save(s, 'JPEG', quality=100) 
            s.seek(0) 
            value.file = s 
        except: 
            return (value, self.error_message) 
        else: 
            return (value, None)
            
def THUMB(image, nx=120, ny=120):
    from PIL import Image 
    import os  
    img = Image.open(request.folder + 'uploads/' + image)
    img.thumbnail((nx,ny), Image.ANTIALIAS) 
    root,ext = os.path.splitext(image)
    thumb='%s_thumb%s' %(root, ext)
    img.save(request.folder + 'uploads/' + thumb)
    print thumb
    return thumb

    
db.image.show.requires=IS_IN_DB(db,db.show.id,'%(name)s')
db.image.id.readable=False
db.image.file.represent=lambda file,row: A(IMG(_src=URL('download',args=file),_height="120"),_href=URL('show_image',args=row.id, vars=request.vars))
db.image.show.represent=lambda show, row:db.show[show].name
db.image.size.represent=lambda size, row:no_none(size)
db.image.media.represent=lambda media, row:no_none(media)
db.image.title.label='Image name'
db.image.file.label=' '
db.image.thumb.label=' '
db.image.thumb.compute=lambda r:THUMB(r['file'])
db.image.thumb.represent=lambda thumb,row: A(IMG(_src=URL('download',args=thumb),_height="120"),_href=URL('show_image',args=row.id, vars=request.vars))
