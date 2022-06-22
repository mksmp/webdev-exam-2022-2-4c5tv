import os
from flask import Flask, render_template, abort, send_from_directory, render_template, request
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

from models import BookGenre, Image
from tools import BooksFilter
from books import PER_PAGE, search_params

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    books = BooksFilter(**search_params()).perform()
    pagination = books.paginate(page, PER_PAGE)
    books = pagination.items
    imgs_arr = []
    genres_arr = []
    for book in books:
        img = Image.query.filter_by(book_id=book.id).first()
        imgs_arr.append(img.url)
        genres_quer = BookGenre.query.filter_by(book_id=book.id).all()
        genres = []
        for genre in genres_quer:
            genres.append(genre.genre.name)
        genres_str = ', '.join(genres)
        genres_arr.append(genres_str)
        

    return render_template('books/index.html', books=books, pagination=pagination, search_params=search_params(), imgs=imgs_arr, genres=genres_arr)



@app.route('/media/images/<image_id>')
def image(image_id):
    image = Image.query.get(image_id)
    if image is None:
        abort(404)
    return send_from_directory(app.config['UPLOAD_FOLDER'], image.storage_filename)
