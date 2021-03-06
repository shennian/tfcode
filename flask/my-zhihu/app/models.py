from . import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    email = db.Column(db.String(128), unique=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer)
    introduction_words = db.Column(db.String(64))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verity_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            u = User(name=forgery_py.internet.user_name(True),
                     email=forgery_py.internet.email_address(),
                     password=forgery_py.lorem_ipsum.word(),
                     role_id=2)
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    @staticmethod
    def add_fake_introduction_words():
        import forgery_py
        for user in User.query.all():
            user.introduction_words = forgery_py.lorem_ipsum.sentences(1)
            #db.session.update(user)
        db.session.commit()

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    permissions = db.Column(db.Integer, unique=True)

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.Follow |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.Follow |
                          Permission.COMMENT |
                          Permission.WRITE_ARTICLES |
                          Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            db.session.add(role)
        db.session.commit()


class Permission:
    Follow = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80


class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    question_labels_id = db.Column(db.Integer)
    question_title = db.Column(db.String(255))
    question_content = db.Column(db.Text)
    user_id = db.Column(db.Integer)
    time = db.Column(db.TIMESTAMP)

    @staticmethod
    def generate_fake(count=100):
        import forgery_py
        import random
        for i in range(count):
            question = Question(question_labels_id=random.randint(1, 10),
                                question_title=forgery_py.lorem_ipsum.title(random.randint(2, 6)),
                                question_content=forgery_py.lorem_ipsum.words(3),
                                user_id=random.randint(1, 100),
                                time=forgery_py.date.date(True))
            db.session.add(question)
        db.session.commit()


class QuestionLabel(db.Model):
    __tablename__ = 'question_labels'
    id = db.Column(db.Integer, primary_key=True)
    label_id = db.Column(db.Integer)


class Label(db.Model):
    __tablename__ = 'labels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)


class Answer(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    time = db.Column(db.TIMESTAMP)
    answer_content = db.Column(db.Text)

    # relate to question
    question_id = db.Column(db.Integer)
    # comments-collection
    comments_collection_id = db.Column(db.Integer)
    # like_collection
    like_collection_id = db.Column(db.Integer)
    # dislike_collection
    dislike_collection_id = db.Column(db.Integer)


    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py

        seed()
        user_count = User.query.count()
        for i in range(count):

            answer = Answer(user_id=randint(0, user_count-1),
                            time=forgery_py.date.date(True),
                            answer_content=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                            question_id=randint(1, 100),
                            comments_collection_id=randint(1, 100),
                            like_collection_id=randint(1, 100),
                            dislike_collection_id=randint(1, 100))

            db.session.add(answer)
        db.session.commit()


class CommentsCollection(db.Model):
    __tablename__ = 'comments_collection'
    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer)

    @staticmethod
    def generate_fake(count=1000):
        import random
        for i in range(count):
            link = CommentsCollection(
                id=random.randint(1, 100),
                comment_id=random.randint(1, 1000)
            )
            db.session.add(link)
        db.session.commit()


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    time = db.Column(db.TIMESTAMP)
    comment_content = db.Column(db.Text)
    likes_count = db.Column(db.Integer)

    comment_author_id = db.Column(db.Integer)

    @staticmethod
    def generate_fake(count=900):
        import forgery_py
        import random

        for i in range(count):
            comment = Comment(user_id=random.randint(1, 100),
                              time=forgery_py.date.date(True),
                              comment_content=forgery_py.lorem_ipsum.sentences(4),
                              likes_count=random.randint(0, 10),
                              comment_author_id=random.randint(1, 100))
            db.session.add(comment)
            db.session.commit()


class LikeCollection(db.Model):
    __tablename__ = 'like_collection'
    id = db.Column(db.Integer, primary_key=True)
    answer_id = db.Column(db.Integer)


class Like(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    like_collection_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    time = db.Column(db.TIMESTAMP)
    status = db.Column(db.Boolean)


class DisLikeCollection(db.Model):
    __tablename__ = 'dislike_collection'
    id = db.Column(db.Integer, primary_key=True)
    answer_id = db.Column(db.Integer)


class DisLike(db.Model):
    __tablename__ = 'dislikes'
    id = db.Column(db.Integer, primary_key=True)
    dislike_collection_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    time = db.Column(db.TIMESTAMP)
    status = db.Column(db.Boolean)


class Follow(db.Model):
    __tablename__ = 'follows'
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer)
    followed_id = db.Column(db.Integer)
    time = db.Column(db.TIMESTAMP)





























