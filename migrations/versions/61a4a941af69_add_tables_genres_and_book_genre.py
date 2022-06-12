"""Add tables genres and book_genre

Revision ID: 61a4a941af69
Revises: 9e8804d5c5f6
Create Date: 2022-06-13 01:55:35.666000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61a4a941af69'
down_revision = '9e8804d5c5f6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('genres',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_genres')),
    sa.UniqueConstraint('name', name=op.f('uq_genres_name'))
    )
    op.create_table('book_genre',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('book_id', sa.Integer(), nullable=True),
    sa.Column('genre_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], name=op.f('fk_book_genre_book_id_books')),
    sa.ForeignKeyConstraint(['genre_id'], ['genres.id'], name=op.f('fk_book_genre_genre_id_genres')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_book_genre'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('book_genre')
    op.drop_table('genres')
    # ### end Alembic commands ###
