from flask import Flask, render_template, request


from . import auth
from .. import db
from ..models import User


@auth.route("/", methods=['post', 'get'])
def index():
    print request.data
    print request.json
    print request.values
    print request.get_json()
    print "index"
    return render_template('index.html')
