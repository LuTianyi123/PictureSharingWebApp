# -*- encoding = UTF-8 -*-

from nowstagram import app, db
from models import User, Image, Comment
from flask import render_template, redirect, request,flash, get_flashed_messages, send_from_directory
import random, hashlib, json, uuid, os
from flask_login import login_user, logout_user, current_user, login_required
from s3sdk import s3_upload_file

@app.route('/index/')
@app.route('/')
def index():
    paginate = Image.query.order_by(db.desc(Image.id)).paginate(page=1, per_page=10, error_out=False)
    return render_template("index.html", images=paginate.items, has_next=paginate.has_next)


@app.route('/index/images/<int:page>/<int:per_page>/')
def index_images(page, per_page):
    paginate = Image.query.order_by(db.desc(Image.id)).paginate(page=page, per_page=per_page, error_out=False)
    map = {'has_next': paginate.has_next}
    images = []
    for image in paginate.items:
        comments = []
        for i in range(0, min(2, len(image.comments))):
            comment = image.comments[i]
            comments.append({'username':comment.user.username,
                             'user_id':comment.user_id,
                             'content':comment.content})
        comments.append({'comment_len': len(image.comments)})
        imgvo = {'id': image.id,
                 'url': image.url,
                 'comment_count': len(image.comments),
                 'user_id': image.user_id,
                 'username': image.user.username,
                 'head_url':image.user.head_url,
                 'created_date':str(image.created_date),
                 'comments':comments}
        images.append(imgvo)

    map['images'] = images
    return json.dumps(map)


@app.route('/image/<int:image_id>/')
def image(image_id):
    image = Image.query.get(image_id)
    if image == None:
        return redirect('/')
    return render_template('pageDetail.html', image=image)


@app.route('/profile/<int:user_id>/')
@login_required
def profile(user_id):
    user = User.query.get(user_id)
    if user is None:
        return redirect('/')

    paginate = Image.query.filter_by(user_id=user_id).paginate(page=1, per_page=3,error_out=False)
    return render_template('profile.html', user=user, images=paginate.items, has_next=paginate.has_next)


@app.route('/profile/images/<int:user_id>/<int:page>/<int:per_page>/')
def user_images(user_id, page, per_page):
    paginate = Image.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page, error_out=False)
    map = {'has_next':paginate.has_next}
    images = []
    for image in paginate.items:
        imgvo = {'id' : image.id ,
                 'url': image.url,
                 'comment_count' : len(image.comments)}
        images.append(imgvo)

    map['images'] = images
    return json.dumps(map)

@app.route('/regloginpage/')
def regloginpage():
    msg = ''
    for m in get_flashed_messages(with_categories=False, category_filter=['reglogin']):
        msg += m
    return render_template('login.html', msg=msg, next=request.values.get('next'))


def redirect_with_msg(target, msg, category):
    if msg is not None:
        flash(msg, category=category)
    return redirect(target)

@app.route('/login/', methods={'post','get'})
def login():
    username = request.values.get('username').strip()
    password = request.values.get('password').strip()

    if (username == '') | (password == ''):
        return redirect_with_msg('/regloginpage/', u'username or password is null', 'reglogin')

    user = User.query.filter_by(username=username).first()

    if user is None:
        return redirect_with_msg('/regloginpage/', u"username doesn't exist", 'reglogin')

    # check
    m = hashlib.md5()
    m.update(password + user.salt)
    if (m.hexdigest() != user.password ):
        return redirect_with_msg('/regloginpage/', u"password is wrong", 'reglogin')

    login_user(user)

    next = request.values.get('next')
    if (next is not None) and next.startswith('/'):
        return redirect(next)

    return redirect('/')


@app.route('/reg/', methods={'post','get'})
def reg():
    username = request.values.get('username').strip()
    password = request.values.get('password').strip()

    if (username == '') | (password == ''):
        return redirect_with_msg('/regloginpage/',u'username or password is null', 'reglogin')

    user = User.query.filter_by(username = username).first()
    if user != None:
        return redirect_with_msg('/regloginpage/', u'username exists', 'reglogin')

    salt = '.'.join(random.sample('0123456789abcdefghijklmnopqrstuvwxyz', 5))
    m = hashlib.md5()
    m.update(password + salt)
    password = m.hexdigest()
    user = User(username, password, salt)
    db.session.add(user)
    db.session.commit()

    login_user(user)

    next = request.values.get('next')
    if (next is not None) and next.startswith('/'):
        return redirect(next)

    return redirect('/')

@app.route('/logout/')
def logout():
    logout_user()
    return redirect('/')


def save_to_local(file, filename):
    save_dir = app.config['UPLOAD_DIR']
    file.save(os.path.join(save_dir, filename))
    return '/image/' + filename


@app.route('/image/<imagename>')
def view_image(imagename):
    return send_from_directory(app.config['UPLOAD_DIR'],imagename)


@app.route('/upload/', methods = {'post'})
def upload():
    print request.files
    file = request.files['file']
    file_ext = ''
    if file.filename.find('.') > 0:
        file_ext = file.filename.rsplit('.', 1)[1].strip().lower()
    if file_ext in app.config['ALLOWED_EXT']:
        filename = str(uuid.uuid1()).replace('-','') + '.' + file_ext
        url = s3_upload_file(file, filename)
        print url
        if url != None:
            db.session.add(Image(url, current_user.id))
            db.session.commit()
    return redirect('/profile/%d' % current_user.id)


@app.route('/addcomment/', methods={'post'})
@login_required
def add_comment():
    image_id = int(request.values['image_id'])
    content = request.values['content']
    comment = Comment(content, image_id, current_user.id)
    db.session.add(comment)
    db.session.commit()

    return json.dumps({"code":0, "id":comment.id,
                       "content":comment.content,
                       "user_id": current_user.id,
                       "username":comment.user.username,
                       "others": "aa"})

