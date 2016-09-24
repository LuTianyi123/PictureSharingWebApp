# -*- encoding = UTF-8 -*-

from nowstagram import app, db

from flask_script import Manager
from nowstagram.models import User, Image, Comment
import random, unittest
#from test import NowstagramTest

manager = Manager(app)

def get_image_url():
    return 'http://images.nowcoder.com/head/' + str(random.randint(0, 1000)) +'m.png'

@manager.command
def run_test():
    db.drop_all()
    db.create_all()
    tests = unittest.TestLoader.discover('./')
    unittest.TextTestResult.run(tests)


@manager.command
def init_database():
    db.drop_all()
    db.create_all()
    for i in range(0, 100):
        db.session.add(User('User' + str(i + 1), '0000'))
        for j in range(0, 10):
            db.session.add(Image(get_image_url(), i + 1))
            for k in range(0, 5):
                db.session.add(Comment('This is a comment' + str(k), 1 + 10 * i + j, i + 1))

    db.session.commit()

    print "database initialized"

if __name__ == '__main__':
    manager.run()


