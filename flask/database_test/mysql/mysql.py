from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:kqf911@128.199.128.244:3306/sen_flask_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    gender = db.Column(db.String(5))
    password = db.Column(db.String(255), unique=True)


@app.route('/')
def hello_world():
    user = User(name="sen", id=2, email="hha", gender='233', password='234')
    db.session.add(user)
    db.session.commit()
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
