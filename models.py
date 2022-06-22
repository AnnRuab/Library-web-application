from sqlalchemy import Column, Date, Float, ForeignKey, String, text
from sqlalchemy.dialects.mysql import BIGINT, TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from app import db
from sqlalchemy import MetaData, Column, ForeignKey, Integer, Table, Text, Time, String, Boolean, text, UniqueConstraint,\
    Numeric, CheckConstraint, DateTime
from sqlalchemy.orm import relationship


Base = declarative_base()
metadata = Base.metadata

__all__ = (
    'Author', 'Genre', 'Comment', 'Genre', 'Role', 'User', 'Buying'
)


class Author(Base):
    __tablename__ = 'author'

    id = Column(BIGINT, primary_key=True)
    name = Column(String(25), nullable=False)


class Genre(Base):
    __tablename__ = 'genre'

    id = Column(BIGINT, primary_key=True)
    name = Column(String(50), nullable=False)


class Role(Base):
    __tablename__ = 'role'

    id = Column(TINYINT, primary_key=True)
    name = Column(String(25), nullable=False)


class Book(Base):
    __tablename__ = 'book'

    id = Column(BIGINT, primary_key=True)
    name = Column(String(50), nullable=False)
    author = Column(ForeignKey('author.id'), nullable=False, index=True)
    extra_info = Column(String(255))
    genre = Column(ForeignKey('genre.id'), index=True)
    price = Column(Float, nullable=False)

    author1 = relationship('Author')
    genre1 = relationship('Genre')


class User(Base):
    __tablename__ = 'user'

    id = Column(BIGINT, primary_key=True)
    name = Column(String(50), nullable=False)
    password = Column(String(25), nullable=False)
    role = Column(ForeignKey('role.id'), index=True)
    email = Column(String(25), nullable=False)

    role1 = relationship('Role')


class Buying(Base):
    __tablename__ = 'buying'

    id = Column(BIGINT, primary_key=True)
    book_id = Column(ForeignKey('book.id'), nullable=False, index=True)
    user_id = Column(ForeignKey('user.id'), nullable=False, index=True)
    creation_date = Column(Date, server_default=text("(curdate())"))

    book = relationship('Book')
    user = relationship('User')


class Comment(Base):
    __tablename__ = 'comment'

    id = Column(BIGINT, primary_key=True)
    user_id = Column(ForeignKey('user.id'), nullable=False, index=True)
    book_id = Column(ForeignKey('user.id'), nullable=False, index=True)
    extra_info = Column(String(255))
    rating = Column(BIGINT)

    book = relationship('User', primaryjoin='Comment.book_id == User.id')
    user = relationship('User', primaryjoin='Comment.user_id == User.id')


# users_books

t_users_songs = Table(
    'users_songs', Base.metadata,
    Column('user_id', ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False),
    Column('song_id', ForeignKey('songs.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
)