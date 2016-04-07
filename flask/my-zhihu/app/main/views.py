from datetime import datetime
from flask import render_template, session, redirect, url_for

from . import main
from .forms import NameForm
from .. import db
from ..models import User


@main.before_request
def haha():
    session_id = None
    try:
        session_id = session['id']
    except:
        return 'login first'


@main.route("/main", methods=['get', 'post'])
def index():
    print 'shit'
    return render_template("main/main.html")


@main.route('/main/vote', methods=['get', 'post'])
def vote():
    pass


@main.route('/main/comment', methods=['get', 'post'])
def comment():
    pass

