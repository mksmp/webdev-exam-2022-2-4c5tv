import os
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from app import db
from models import Book, BookGenre, Review, User, Genre, Image, Collection, BookCollection
from tools import BooksFilter, ImageSaver, ReviewsFilter
from auth import check_rights
import markdown

bp = Blueprint('books', __name__, url_prefix='/books')

PER_PAGE = 3

COMMENT_PAGE = 5

PER_PAGE_COMMENTS = 10

BOOK_PARAMS = ['author', 'name', 'publisher', 'short_desc', 'year', 'vol_pages']

COMMENT_PARAMS = ['rating', 'text', 'book_id', 'user_id']

COLLECTION_PARAMS = ['name','user_id']

def params():
    return { p: request.form.get(p) for p in BOOK_PARAMS }

def comment_params():
    return { p: request.form.get(p) for p in COMMENT_PARAMS }

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

def selection_params():
    return { p: request.form.get(p) for p in COLLECTION_PARAMS }

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
    db.session.add(book)
    db.session.commit()

    # book = Book.query.filter_by(id)

    f = request.files.get('background_img')
    if f and f.filename:
        img = ImageSaver(f).save(book.id)
    
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
    book.short_desc = markdown.markdown(book.short_desc)
    reviews = Review.query.filter_by(book_id=book_id).limit(COMMENT_PAGE)
    user_review = None
    if current_user.is_authenticated is True:
        user_review = Review.query.filter_by(book_id=book_id, user_id=current_user.id).first()
    users = User.query.all()
    
    genres_quer = BookGenre.query.filter_by(book_id=book_id).all()
    genres = []
    for genre in genres_quer:
        genres.append(genre.genre.name)
    genres = ', '.join(genres)

    img = Image.query.filter_by(book_id=book_id).first()
    img = img.url

    collections = Collection.query.filter_by(user_id=current_user.id).all()


    return render_template('books/show.html', book=book, review=reviews, users=users, user_review=user_review, genres=genres, image=img, collections=collections)


@bp.route('/<int:book_id>/edit')
@login_required
@check_rights('update')
def edit(book_id):
    book = Book.query.filter_by(id=book_id).first()  
    genres = Genre.query.all()
    genres_quer = BookGenre.query.filter_by(book_id=book_id).all()
    genres_select = []
    for genre in genres_quer:
        genres_select.append(genre.genre.id)

    return render_template('books/edit.html', genres=genres, genres_select=genres_select, book=book)


@bp.route('/<int:book_id>/update', methods=['POST'])
@login_required
@check_rights('update')
def update(book_id):
    book = Book.query.filter_by(id=book_id).first() # апдейт книги
    form_dict = params()
    book.name = form_dict['name']
    book.author = form_dict['author']
    book.publisher = form_dict['publisher']
    book.short_desc = form_dict['short_desc']
    book.year = form_dict['year']
    
    genres_old = BookGenre.query.filter_by(book_id=book_id).all() # удаление старых жанров для данной книги
    for gnr in genres_old:
        db.session.delete(gnr)

    genres_arr = request.form.getlist('genre') # добавление новых жанров для данной книги
    for genres in genres_arr:
        book_genre = BookGenre()
        book_genre.book_id = book.id
        book_genre.genre_id = genres
        db.session.add(book_genre)

    db.session.commit()
    return redirect(url_for('index'))


@login_required
@bp.route('/<int:book_id>/delete', methods=['POST'])
@check_rights('delete')
def delete(book_id):
    book = Book.query.filter_by(id=book_id).first()
    book_name = book.name
    img = Image.query.filter_by(book_id=book_id).first()
    img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'images') + '\\' + img.storage_filename
    db.session.delete(book)
    db.session.commit()
    os.remove(img_path)
    flash(f'Книга {book_name} была успешно удалена!', 'success')
    return redirect(url_for('index'))



@bp.route('/<int:book_id>', methods=['POST'])
@login_required
def send_comment(book_id):
    reviews = Review(**comment_params())
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

@bp.route('/collections')
@login_required
@check_rights('check_collections')
def collections():
    collections = Collection.query.filter_by(user_id=current_user.id).all()
    return render_template('books/collections.html', endpoint = 'collections', collections=collections)

@bp.route('/collections/<int:user_id>', methods=['POST'])
@login_required
@check_rights('check_collections')
def create_collection(user_id):
    collection = Collection(**selection_params())
    collection.user_id = user_id
    db.session.add(collection)
    db.session.commit()
    flash(f'Подборка {collection.name} была успешно добавлена!', 'success')
    return redirect(url_for('books.collections'))

@bp.route('/add_to_collection/<int:book_id>', methods=['POST'])
@login_required
@check_rights('check_collections')
def add_to_collection(book_id):
    collection_id = request.form.get('collection')
    
    # тут прописать проверку
    # if 
    #     flash(f'Эта книга уже есть в выбранной подборке!', 'danger')
    #     return redirect(url_for('books.show', book_id=book_id))
    
    add_book = BookCollection()
    add_book.book_id = book_id
    add_book.collection_id = collection_id
    db.session.add(add_book)
    db.session.commit()
    flash(f'Книга была успешно добавлена в подборку!', 'success')
    return redirect(url_for('books.show', book_id=book_id))