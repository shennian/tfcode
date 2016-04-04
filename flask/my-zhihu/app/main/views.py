from datetime import datetime
from flask import render_template, session, redirect, url_for

from . import main
from .forms import NameForm
from .. import db
from ..models import User


@main.route("/", methods=['get', 'post'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        return "yes"
    return render_template("main/index.html", form=form)
