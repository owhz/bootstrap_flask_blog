import os

from flask_migrate import Migrate, upgrade, current_app
from dotenv import load_dotenv


flask_env = os.environ.get('FLASK_ENV')

if not flask_env:
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)


from app import create_app
from app.models import db, User, Post


app = create_app(os.getenv('FLASK_ENV') or 'default')
Migrate(app, db)


@app.shell_context_processor
def make_context():
    return dict(db=db, User=User, Post=Post)


@app.cli.command()
def test():
    pass


@app.cli.command()
def deploy():
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
