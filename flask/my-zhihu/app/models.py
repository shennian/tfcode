from . import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    email = db.Column(db.String(128), unique=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verity_password(self, password):
        return check_password_hash(self.password_hash, password)


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


class CommentsCollection(db.Model):
    __tablename__ = 'comments_collection'
    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    time = db.Column(db.TIMESTAMP)
    comment_content = db.Column(db.Text)
    likes_count = db.Column(db.Integer)

    comment_author_id = db.Column(db.Integer)


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





























