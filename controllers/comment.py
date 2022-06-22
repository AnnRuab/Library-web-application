from app import *
from models import *
from flask import render_template, flash, abort


@app.route('/comment/<comment_id>')
@login_required
def comment(comment_id):
    comment = Comment.query.get(comment_id)
    return render_template('author.html',
                           title='search_author',
                           extra_info=comment.extra_info,
                           rating=comment.rating)

#
# @app.route('/comment_delete')
# @login_required
# def comment_delete(comment_id, prev, t_user_):
#     comment = Comment.query.get(comment_id)
#     if comment:
#         comments = db.session.query.get(Comment).filter(Comment.user.any(User.id == current_user.id))
#         if comment in comments:
#             flash('Така книга вже додана')
#             if prev == 'search':
#                 return redirect(url_for('book', book_id=book.id))
#             elif prev == 'search_res':
#                 return redirect(url_for('library'))
#             else:
#                 return redirect(url_for('library'))
#
#         flash('Книга {0} додана!'.format(book.name))
#         statement = t_user_book.insert().values(user_id=current_user.id, book_id=book.id)
#         db.session.execute(statement)
#         db.session.commit()
#
#         if prev == 'search':
#             return redirect(url_for('library', book_id=book_id))
#         else:
#             return redirect(url_for('library'))
#
#     abort(404)