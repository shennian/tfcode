# -*- coding: utf-8 -*-
from datetime import datetime
from flask import render_template, session, redirect, url_for, request

from . import main
from .forms import NameForm
from .. import db
from ..models import User, Answer, Question, CommentsCollection, Comment

'''
@main.before_request
def haha():
    session_id = None
    try:
        session_id = session['id']
    except:
        return 'login first'
'''


@main.route("/main", methods=['get', 'post'])
def index():
    print 'shit'

    answers = Answer.query.order_by(Answer.time.desc()).limit(10).all()
    import datetime
    now_time = datetime.datetime.now()
    for answer in answers:
        dtime = (now_time - answer.time).total_seconds()
        print dtime
        # day
        if dtime > 60 * 24 * 60:
            answer.time = str(int(dtime / (60 * 24 * 60))) + "天前"
        elif dtime > 60 * 60:
            answer.time = str(int(dtime / (60 * 60))) + '小时前'
        elif dtime > 60:
            answer.time = str(int(dtime / 60)) + '分前'
        elif dtime:
            answer.time = str(dtime) + '秒前'
        answer.time = unicode(answer.time, "utf8")

        setattr(answer, 'answer_id', answer.id)
        setattr(answer, 'username', User.query.filter_by(id=answer.user_id).first().name)
        setattr(answer, 'introduction_words', User.query.filter_by(id=answer.user_id).first().introduction_words)
        setattr(answer, 'question_title', Question.query.filter_by(id=answer.question_id).first().question_title)

    return render_template("main/main.html", posts=answers)


@main.route('/main/vote', methods=['get', 'post'])
def vote():
    pass


@main.route('/main/comment', methods=['get', 'post'])
def comment():
    request_data = request.args.to_dict()
    answer_id = request_data['answer_id']
    answer = Answer.query.filter_by(id=answer_id).first()
    comments_collection_id = answer.comments_collection_id
    all_comments_collection = CommentsCollection.query.filter_by(id=comments_collection_id).all()
    result = {}
    for collection in all_comments_collection:
        comment_id = collection.comment_id
        

    pass

