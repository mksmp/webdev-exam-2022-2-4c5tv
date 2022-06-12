import os
from flask import Flask, render_template, send_file, abort, send_from_directory
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
application = app

app.config.from_pyfile('config.py')


convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db)

from books import bp as books_bp
from auth import bp as auth_bp, init_login_manager

app.register_blueprint(auth_bp)
app.register_blueprint(books_bp)


init_login_manager(app)

from models import User, Image

@app.route('/')
def index():
    # categories = Category.query.all() # Добавить жанры вместо категорий
    return render_template(
        'index.html',
        categories=categories,
    )


@app.route('/media/images/<image_id>')
def image(image_id):
    image = Image.query.get(image_id)
    if image is None:
        abort(404)
    # return send_file(os.path.join(app.config['UPLOAD_FOLDER'], image.storage_filename))
    return send_from_directory(app.config['UPLOAD_FOLDER'], image.storage_filename)
