from flask import render_template, flash, abort

from app import *
from models import *


@app.route('/<prev>/book/<book_id>/add')
def book_add(book_id, prev, t_user_book=None):
    book = Book.query.get(book_id)

    if book:
        books = db.session.query(Book).filter(Book.users.any(User.id == current_user.id))

        if book in books:
            flash('Така книга вже додана')
            if prev == 'search':
                return redirect(url_for('book', book_id=book.id))
            elif prev == 'search_res':
                return redirect(url_for('library'))
            else:
                return redirect(url_for('library'))

        flash('Книга {0} додана!'.format(book.name))
        statement = t_user_book.insert().values(user_id=current_user.id, book_id=book.id)
        db.session.execute(statement)
        db.session.commit()

        if prev == 'search':
            return redirect(url_for('library', book_id=book_id))
        else:
            return redirect(url_for('library'))

    abort(404)


@app.route('/<prev>/book/<book_id>/delete')
def book_delete(book_id, prev):
    book = db.session.query(Book).get(book_id)

    if book:
        books = db.session.query(Book).filter(Book.users.any(User.id == current_user.id))

        if book not in books:
            flash('Такої книги немає!')
            if prev == 'search':
                return redirect(url_for('library', book_id=book_id))
            elif prev == 'search_res':
                return redirect(url_for('library'))
            elif prev == 'profile':
                return redirect(url_for('profile'))
            else:
                return redirect(url_for('library'))

        flash('Книга {0} видалена!'.format(book.name))
        book.users.remove(current_user)
        db.session.commit()

        if prev == 'search':
            return redirect(url_for('library', book_id=book_id))
        elif prev == 'profile':
            return redirect(url_for('profile'))
        else:
            return redirect(url_for('library'))

    abort(404)
