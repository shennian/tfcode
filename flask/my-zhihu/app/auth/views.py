from flask import Flask, render_template, request, session


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
    font = ImageFont.truetype("/usr/share/fonts/default/TrueType/georgia.ttf", 30)
    draw.text((5, 10), s, font=font, fill='#ff0000')
    image.save(os.path.join(os.path.dirname("__file__"), os.path.pardir) + '/static/' + s + '.png')
    return s


@auth.route("/", methods=['post', 'get'])
def index():
    print create_check_code()
    return render_template('index.html')


@auth.route('/register', methods=['post'])
def register():
    request_data = request.args.to_dict()
    fields = ['name', 'email', 'password', 'check_code']
    if check_post_data(request_data, fields) is False:
        return {'status': False, 'Message': 'json_format_error'}

    if session['check_code'] != request_data['check_code']:
        return {'status': False, 'Message': 'check_code_error'}

    user = User.query.filter_by(email=request_data['email']).first()
    if user is not None:
        return {'status': False, 'Message': 'email exists'}
    user = User(name=request_data['name'], email=request_data['email'],
                password=request_data['password'], role_id=2)
    db.session.add(user)
    db.session.commit()
    return {'status': True, 'Message': 'register successfully'}


@auth.route('/login', methods=['post'])
def login():
    request_data = request.args.to_dict()
    fields = ['email', 'password', 'check_code']
    if check_post_data(request_data, fields) is False:
        return {'status': False, 'Message': 'json_format_error'}

    if session['check_code'] != request_data['check_code']:
        return {'status': False, 'Message': 'check_code_error'}

    user = User.query.filter_by(email=request_data['email']).first()
    if user is not None and user.verity_password(request_data['password']):
        return "fuck"
    else:
        return "用户名或者密码错误"