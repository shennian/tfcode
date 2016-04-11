from flask import Flask, render_template, request, session, redirect, url_for


from . import auth
from .. import db
from ..models import User


def check_post_data(data, fields):
    data_keys = data.keys()
    if len(data_keys) != len(fields):
        return False

    for key in data_keys:
        if key not in fields:
            return False
    return True


def create_check_code():
    from PIL import Image, ImageDraw, ImageFont
    import os, random
    s = ''
    for i in range(6):
        s += str(random.randint(1, 9))
    image = Image.new("RGBA", (100, 50), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("simsun.ttc", 30)
    draw.text((5, 10), s, font=font, fill='#ff0000')
    print os.path.abspath('.') + '/app/static/' + s + '.png'
    image.save(os.path.abspath('.') + '/app/static/' + s + '.png')
    return s


@auth.route("/", methods=['post', 'get'])
def index():
    check_code = create_check_code()
    session['check_code'] = check_code
    return render_template('index.html', check_code=check_code+'.png')


@auth.route('/register', methods=['post', 'get'])
def register():
    print 'register'
    request_data = request.args.to_dict()
    print request_data
    fields = ['name', 'email', 'password', 'check_code']
    if check_post_data(request_data, fields) is False:
        return {'status': False, 'Message': 'json_format_error'}.__repr__()

    if session['check_code'] != request_data['check_code']:
        return {'status': False, 'Message': 'check_code_error'}.__repr__()

    user = User.query.filter_by(email=request_data['email']).first()
    if user is not None:
        return {'status': False, 'Message': 'email exists'}
    user = User(name=request_data['name'], email=request_data['email'],
                password=request_data['password'], role_id=3)
    db.session.add(user)
    db.session.commit()
    return {'status': True, 'Message': 'register successfully'}.__repr__()


@auth.route('/login', methods=['post', 'get'])
def login():
    request_data = request.args.to_dict()
    fields = ['email', 'password', 'check_code']
    if check_post_data(request_data, fields) is False:
        return {'status': False, 'Message': 'json_format_error'}.__repr__()

    if session['check_code'] != request_data['check_code']:
        return {'status': False, 'Message': 'check_code_error'}.__repr__()

    user = User.query.filter_by(email=request_data['email']).first()
    if user is not None and user.verity_password(request_data['password']):
        return {'status': True, 'Message': 'login successfully'}.__repr__()
    else:
        return "user name or password error"