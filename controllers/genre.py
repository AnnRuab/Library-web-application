from flask import render_template

from app import *
from models import *

@app.route('/genre/<genre_id>')
def genre(genre_id):
    genre = Genre.query.get(genre_id)
    author = Author.guery.with_entities(Author.firstname,
                                        Author.surname,
                                        Author.id).filter(Author.genre_id == genre_id).all()
    return render_template('genre.html', title='genre', genre=genre.name, author=author)