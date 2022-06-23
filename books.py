import os
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from app import db
from models import Book, BookGenre, Review, User, Genre, Image, Collection, BookCollection
from tools import ImageSaver, ReviewsFilter
from auth import check_rights
import markdown
import bleach

bp = Blueprint('books', __name__, url_prefix='/books')

PER_PAGE = 3

COMMENT_PAGE = 5

PER_PAGE_COMMENTS = 10

BOOK_PARAMS = ['author', 'name', 'publisher',
               'short_desc', 'year', 'vol_pages']

COMMENT_PARAMS = ['rating', 'text', 'book_id', 'user_id']

COLLECTION_PARAMS = ['name', 'user_id']


def params():
    return {p: request.form.get(p) for p in BOOK_PARAMS}


def comment_params():
    return {p: request.form.get(p) for p in COMMENT_PARAMS}


def search_params():
    return {
        'name': request.args.get('name')
    }


def search_params_comm(book_id, req_form=None):
    return {
        'name': request.args.get('name'),
        'book_id': book_id,
        'sort': req_form
    }


def collection_params():
    return {p: request.form.get(p) for p in COLLECTION_PARAMS}


@bp.route('/new')
@check_rights('create')
@login_required
def new():
    genres = Genre.query.all()
    return render_template('books/new.html', genres=genres)


@bp.route('/create', methods=['POST'])
@check_rights('create')
@login_required
def create():
    book = Book(**params())
    # экранирование запрещенных тегов
    book.short_desc = bleach.clean(book.short_desc)
    db.session.add(book)
    db.session.commit()

    f = request.files.get('background_img')
    if f and f.filename:
        img = ImageSaver(f).save(book.id)

    # добавление выбранных жанров из multiple списком id
    genres_arr = request.form.getlist('genre')
    for genres in genres_arr:
        book_genre = BookGenre()
        book_genre.book_id = book.id
        book_genre.genre_id = genres
        db.session.add(book_genre)

    db.session.commit()

    flash(f'Книга {book.name} была успешно добавлена!', 'success')
    return redirect(url_for('index'))


@bp.route('/<int:book_id>')
def show(book_id):
    book = Book.query.get(book_id)
    # преобразование текста из html в markdown
    book.short_desc = markdown.markdown(book.short_desc)
    reviews = Review.query.filter_by(book_id=book_id).limit(
        COMMENT_PAGE)  # подгружаем несколько отзывов
    user_review = None
    if current_user.is_authenticated is True:
        # проверка написал ли пользователь данной сессии комментарий
        user_review = Review.query.filter_by(
            book_id=book_id, user_id=current_user.id).first()

    genres_quer = BookGenre.query.filter_by(
        book_id=book_id).all()  # берем все жанры у этой книги
    genres = []
    for genre in genres_quer:
        genres.append(genre.genre.name)
    genres = ', '.join(genres)

    # подгружаем картинку книги
    img = Image.query.filter_by(book_id=book_id).first()
    img = img.url
    
    if current_user.is_authenticated is True and current_user.is_user is True:
        collections = Collection.query.filter_by(user_id=current_user.id).all()
    else:
        collections = None

    return render_template('books/show.html', book=book, review=reviews, user_review=user_review, genres=genres, image=img, collections=collections)


@bp.route('/<int:book_id>/edit')
@login_required
@check_rights('update')
def edit(book_id):
    book = Book.query.get(book_id)
    genres = Genre.query.all()
    genres_quer = BookGenre.query.filter_by(book_id=book_id).all() # выбранные жанры у книги
    genres_select = []
    for genre in genres_quer:
        genres_select.append(genre.genre.id)

    return render_template('books/edit.html', genres=genres, genres_select=genres_select, book=book)


@bp.route('/<int:book_id>/update', methods=['POST'])
@login_required
@check_rights('update')
def update(book_id):
    book = Book.query.filter_by(id=book_id).first()  # апдейт книги
    form_dict = params()
    book.name = form_dict['name']
    book.author = form_dict['author']
    book.publisher = form_dict['publisher']
    book.short_desc = form_dict['short_desc']
    # экранирование запрещенных тегов
    book.short_desc = bleach.clean(book.short_desc)
    book.year = form_dict['year']

    # удаление старых жанров для данной книги
    genres_old = BookGenre.query.filter_by(book_id=book_id).all()
    for gnr in genres_old:
        db.session.delete(gnr)

    # добавление новых жанров для данной книги
    genres_arr = request.form.getlist('genre')
    for genres in genres_arr:
        book_genre = BookGenre()
        book_genre.book_id = book.id
        book_genre.genre_id = genres
        db.session.add(book_genre)

    db.session.commit()
    # flask()
    return redirect(url_for('index'))


@bp.route('/<int:book_id>/delete', methods=['POST'])
@login_required
@check_rights('delete')
def delete(book_id):
    book = Book.query.filter_by(id=book_id).first()
    book_name = book.name
    img = Image.query.filter_by(book_id=book_id).first()
    img_path = os.path.join(os.path.dirname(os.path.abspath(
        __file__)), 'media', 'images') + '\\' + img.storage_filename # удаление картинки из папки media
    db.session.delete(book)
    db.session.commit()
    os.remove(img_path)
    flash(f'Книга {book_name} была успешно удалена!', 'success')
    return redirect(url_for('index'))


@bp.route('/<int:book_id>', methods=['POST'])
@login_required
def send_comment(book_id):
    reviews = Review(**comment_params())
    # экранирование запрещенных тегов
    reviews.text = bleach.clean(reviews.text)
    books = Book.query.filter_by(id=book_id).first()
    books.rating_num += 1
    books.rating_sum += int(reviews.rating)
    db.session.add(reviews)
    db.session.commit()
    flash('Комментарий был успешно добавлен!', 'success')
    return redirect(url_for('books.show', book_id=books.id))


@bp.route('/<int:book_id>/reviews')
def reviews(book_id):
    page = request.args.get('page', 1, type=int)
    sort = request.args.get('sort')
    reviews = ReviewsFilter(book_id).sort_reviews(sort)
    books = Book.query.filter_by(id=book_id).first()
    pagination = reviews.paginate(page, PER_PAGE_COMMENTS)
    reviews = pagination.items
    return render_template('books/reviews.html', reviews=reviews, books=books, req_form=sort, pagination=pagination, search_params=search_params_comm(book_id, sort))


@bp.route('/user_collections')
@login_required
@check_rights('check_collections')
def collections():
    collections = Collection.query.filter_by(user_id=current_user.id).all()
    collect_arr = [] # счетчик книг в подборке
    for collection in collections:
        collection_id = collection.id
        count_query = BookCollection.query.filter_by(collection_id=collection_id).all()
        collect_arr.append(len(count_query))
    return render_template('books/collections.html', endpoint='collections', collections=collections, collect_arr=collect_arr)


@bp.route('/user_collection/<int:user_id>/create_collection', methods=['POST'])
@login_required
@check_rights('check_collections')
def create_collection(user_id):
    collection = Collection(**collection_params())
    collection.user_id = user_id
    db.session.add(collection)
    db.session.commit()
    flash(f'Подборка {collection.name} была успешно добавлена!', 'success')
    return redirect(url_for('books.collections'))


@bp.route('/user_collection/<int:book_id>/add_to_collection', methods=['POST'])
@login_required
@check_rights('check_collections')
def add_to_collection(book_id):
    collection_id = request.form.get('collection')
    check_book_in_collection = BookCollection.query.filter_by(collection_id=collection_id, book_id=book_id).one_or_none()

    if check_book_in_collection is not None:
        flash(f'Эта книга уже есть в выбранной подборке!', 'danger')
        return redirect(url_for('books.show', book_id=book_id))

    add_book = BookCollection()
    add_book.book_id = book_id
    add_book.collection_id = collection_id
    db.session.add(add_book)
    db.session.commit()
    flash(f'Книга была успешно добавлена в подборку!', 'success')
    return redirect(url_for('books.show', book_id=book_id))


@bp.route('/user_collection/<int:collection_id>')
@login_required
@check_rights('check_collections')
def show_user_collection(collection_id):
    books_ids = []
    take_collection = BookCollection.query.filter_by(collection_id=collection_id).all()
    for collection in take_collection:
        books_ids.append(collection.book_id)
    books = []
    for book_id in books_ids:
        book = Book.query.get(book_id)
        books.append(book)
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
    return render_template('books/user_collection.html', books=books, search_params=search_params(), imgs=imgs_arr, genres=genres_arr)
