from crypt import methods
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from app import db
from models import Book, Review, User
from tools import BooksFilter, ImageSaver, ReviewsFilter

bp = Blueprint('books', __name__, url_prefix='/books')

PER_PAGE = 3

COMMENT_PAGE = 5

PER_PAGE_COMMENTS = 10

BOOK_PARAMS = ['author', 'name', 'publisher', 'short_desc', 'full_desc', 'year', 'vol_pages']

COMMENT_PARAMS = ['rating', 'text', 'book_id', 'user_id']


def params():
    return { p: request.form.get(p) for p in BOOK_PARAMS }


def comment_params():
    return { p: request.form.get(p) for p in COMMENT_PARAMS }

def search_params():
    return {
        'name': request.args.get('name'),
        'genre_ids': request.args.getlist('genre_ids')
    }

def search_params_comm(book_id):
    return {
        'name': request.args.get('name'),
        'book_id': book_id
    }