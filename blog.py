import os

from flask_migrate import Migrate

from app import create_app
from app.models import Post, User, db


app = create_app(os.getenv('FLASK_ENV') or 'default')
Migrate(app, db)


@app.shell_context_processor
def make_context():
    return dict(db=db, User=User, Post=Post)


if __name__ == '__main__':
    app.run(debug=True)
