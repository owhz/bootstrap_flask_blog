import os

from flask_migrate import Migrate, current_app, upgrade

from app import create_app
from app.models import Post, User, db


app = create_app(os.getenv('FLASK_ENV') or 'default')
Migrate(app, db)


@app.shell_context_processor
def make_context():
    return dict(db=db, User=User, Post=Post)


@app.cli.command()
def test():
    pass


@app.cli.command()
def init_amdin_user():
    upgrade()
    db.create_all()
    user = User.query.filter_by(email=current_app.config['BLOG_ADMIN_EMAIL']).first()
    if not user:
        user = User(email=current_app.config['BLOG_ADMIN_EMAIL'],
                    username=current_app.config['BLOG_ADMIN_USERNAME'],
                    password=current_app.config['BLOG_ADMIN_PASSWORD'])
        db.session.add(user)
        db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)
