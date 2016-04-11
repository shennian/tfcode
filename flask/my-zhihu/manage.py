import os
from app import create_app, db
from app.models import User, Role
from flask.ext.script import Manager, Shell

app = create_app('test')
manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)

manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    '''
    manager.add_command("shell", Shell(make_context=make_shell_context))
    print 'fuck'
    app.run()
    '''
    manager.run()
    #app.run()
