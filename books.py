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


def search_params_comm(book_id, req_form=None):
    return {
        'name': request.args.get('name'),
        'book_id': book_id,
        'sort': req_form
    }

def collection_paginate_params(collection_id):
    return {'collection_id': collection_id}

def collection_params(user_id):
    dict_collection = {p: request.form.get(p) for p in COLLECTION_PARAMS}
    dict_collection['user_id'] = user_id
    return dict_collection

def add_book_to_collection_params(book_id, collection_id):
    return {
        'book_id': book_id,
        'collection_id': collection_id
    }

def add_genre_to_book(book_id, genre_id):
    return {
        'book_id': book_id,
        'genre_id': genre_id
    }


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
    try:
        db.session.add(book)
        db.session.commit()
    except:
        db.session.rollback()
        flash('При сохранении книги произошла ошибка. Проверьте введённые данные.', 'danger')
        return redirect(url_for('books.new'))

    f = request.files.get('background_img')
    if f and f.filename:
        img = ImageSaver(f).save(book.id)
        if img == None:
            db.session.delete(book)
            db.session.commit()
            flash('Нельзя использовать книгу с обложкой, которая уже имеется!', 'danger')
            return redirect(url_for('books.new'))
    # добавление выбранных жанров из multiple списком id
    genres_arr = request.form.getlist('genre')
    for genres in genres_arr:
        book_genre = BookGenre(**add_genre_to_book(book.id, genres))
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
    for review in reviews:
        review.text = markdown.markdown(review.text)
    user_review = None
    if current_user.is_authenticated is True:
        # проверка написал ли пользователь данной сессии комментарий
        user_review = Review.query.filter_by(
            book_id=book_id, user_id=current_user.id).first()
        
        if user_review:
            user_review.text = markdown.markdown(user_review.text)

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
        book_genre = BookGenre(**add_genre_to_book(book.id, genres))
        db.session.add(book_genre)

    db.session.commit()
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

    book = Book.query.filter_by(id=book_id).first()
    book.rating_num += 1
    book.rating_sum += int(reviews.rating)
    try:
        db.session.add(reviews)
        db.session.commit()
    except:
        db.session.rollback()
        flash(f'Не удалось добавить комментарий!', 'danger')
        return redirect(url_for('books.show', book_id=book.id))
    flash('Комментарий был успешно добавлен!', 'success')
    return redirect(url_for('books.show', book_id=book.id))


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
        collect_arr.append(len(BookCollection.query.filter_by(collection_id=collection.id).all()))
    return render_template('books/collections.html', endpoint='collections', collections=collections, collect_arr=collect_arr)


@bp.route('/user_collection/<int:user_id>/create_collection', methods=['POST'])
@login_required
@check_rights('check_collections')
def create_collection(user_id):
    collection = Collection(**collection_params(user_id))
    try:
        db.session.add(collection)
        db.session.commit()
    except:
        db.session.rollback()
        flash(f'Не удалось создать коллекцию!', 'danger')
        return redirect(url_for('books.collections'))
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

    add_book = BookCollection(**add_book_to_collection_params(book_id, collection_id))
    try:
        db.session.add(add_book)
        db.session.commit()
    except:
        db.session.rollback()
        flash(f'Не удалось добавить книгу в подборку!', 'danger')
        return redirect(url_for('books.show', book_id=book_id))
    flash(f'Книга была успешно добавлена в подборку!', 'success')
    return redirect(url_for('books.show', book_id=book_id))


@bp.route('/user_collection/<int:collection_id>')
@login_required
@check_rights('check_collections')
def show_user_collection(collection_id):
    page = request.args.get('page', 1, type=int)
    take_collection = BookCollection.query.filter_by(collection_id=collection_id)
    pagination = take_collection.paginate(page, PER_PAGE)
    items = pagination.items
    books = []
    for collection in items:
        books.append(collection.book)
    imgs_arr, genres_arr = take_info_for_card_book(books)
    return render_template('books/user_collection.html', books=books, pagination=pagination, imgs=imgs_arr, genres=genres_arr, params=collection_paginate_params(collection_id))

def take_info_for_card_book(books):
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
    return imgs_arr, genres_arr