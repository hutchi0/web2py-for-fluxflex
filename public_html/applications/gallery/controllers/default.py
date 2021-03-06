# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


from gluon.contenttype import contenttype
import os

def test1():
    from PIL import Image
    THUMB('image.file.859d3572e80c621e.4379636c616d656e202e6a7067.jpg')
    return dict()

def index():
    return dict(personal=db.personal[1])

def biography():
    return dict(personal=db.personal[1])

def contact():
    return dict(personal=db.personal[1])

def show():
    try: 
        show_id=int(request.args[0])
        title=db(db.show.id==show_id).select(db.show.name)[0].name
    except: redirect(URL(r=request,f='index'))
    images=db(db.image.show==show_id).select()
    return dict(title=title,images=images)
    
@auth.requires_login()
def edit_images():
    fields=(db.image.id,db.image.title,db.image.show,db.image.size,
            db.image.media,db.image.price,db.image.thumb)
    table=SQLFORM.grid(db.image,fields=fields)
    return dict(table=table)

@auth.requires_login()
def edit_galleries():
    table=SQLFORM.grid(db.show)
    return dict(table=table)

@auth.requires_login()
def edit_personal():
    table=SQLFORM.grid(db.personal)
    return dict(table=table)



def download():
    filename=request.args[0]
    response.headers['Content-Type']=contenttype(filename)
    return open(os.path.join(request.folder,'uploads/','%s' % filename),'rb').read()





def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

#
#def download():
#    """
#    allows downloading of uploaded files
#    http://..../[app]/default/download/[filename]
#    """
#    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs bust be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())


def category():

    iconup = IMG(_src=URL('static','images',args='up.png') )    
    icondown = IMG(_src=URL('static','images',args='down.png') )    
    
    fields=[db.image.thumb,db.image.title,db.image.size,db.image.media,db.image.id,
            db.image.price]
    headers={'album_name.label':'albumx name', 'image':''}

    show=db.show(request.args(0))
    table=SQLFORM.grid(db.image.show==show,fields=fields,deletable=False,
                       editable=False,details=False,create=False,csv=False,searchable=False,
                       orderby='title',sorter_icons=(iconup, icondown),paginate=20) 

    return dict(table=table, title=show.name)

def show_image():
    image = db.image(request.args(0))
    return dict(image=image, category=category)


def next_image():
    row=db.image[request.args(0)]
    previous_hit = False
    print row.show
    
    images=db(db.image.show==row.show).select()
    id=images.first().id
    for image in images:  
        if previous_hit==True:
            id=image.id
            break
        if image.id == int(request.args(0)):
            previous_hit = True
    redirect(URL('show_image',args=id, vars=request.vars))
  
def previous_image():
    row=db.image[request.args(0)]
    previous_hit = False
    print row.show
    
    images=db(db.image.show==row.show).select()
    id=images.last().id
    for image in images:  
        if image.id == int(request.args(0)):
            break
        id=image.id
        
    redirect(URL('show_image',args=id, vars=request.vars))
    
def categories():
    table=SQLFORM.grid(db.show,deletable=False,
                       editable=False,details=False,create=False,csv=False,searchable=False,
                       orderby='name',paginate=20) 
    
    return dict(table=table)
