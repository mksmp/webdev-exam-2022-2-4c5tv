import sqlalchemy as sa
from sqlalchemy.dialects import mysql
import os
from app import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin 
from flask import url_for

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    desciption = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100), nullable=False)
    login = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), unique=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    created_at = db.Column(db.DateTime, nullable=False, server_default=sa.sql.func.now())

    role = db.relationship('Role')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def full_name(self):
        return ' '.join([self.last_name, self.first_name, self.middle_name or ''])

    def __repr__(self):
        return '<User %r>' % self.login

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    short_desc = db.Column(db.Text, nullable=False)
    full_desc = db.Column(db.Text, nullable=False)
    rating_sum = db.Column(db.Integer, nullable=False, default=0)
    rating_num = db.Column(db.Integer, nullable=False, default=0)
    year = db.Column(mysql.YEAR, nullable=False)
    publisher = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    vol_pages = db.Column(db.Integer, nullable=False, default=0)

    bg_image = db.relationship('Image')

    def __repr__(self):
        return '<Book %r>' % self.name
    
    @property
    def rating(self):
        if self.rating_num > 0:
            return self.rating_sum / self.rating_num
        return 0

class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.String(100), primary_key=True)
    file_name = db.Column(db.String(100), nullable=False)
    mime_type = db.Column(db.String(100), nullable=False)
    md5_hash = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False, server_default=sa.sql.func.now())
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))

    book_img = db.relationship('Book')


    def __repr__(self):
        return '<Book %r>' % self.file_name

    @property
    def storage_filename(self):
        _, ext = os.path.splitext(self.file_name)
        return self.id + ext

    @property
    def url(self):
        return url_for('image', image_id = self.id)

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=sa.sql.func.now())
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    book = db.relationship('Book')
    user = db.relationship('User')

    def __repr__(self):
        return '<Review %r>' % self.text

class Genre(db.Model):
    __tablename__ = 'genres'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return '<Genre %r>' % self.name

class BookGenre(db.Model):
    __tablename__ = 'book_genre'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'))

    book = db.relationship('Book')
    genre = db.relationship('Genre')

    def __repr__(self):
        return '<GenresOfBook %r>' % self.id