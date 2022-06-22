from app import *
from models import *
from itertools import groupby


@app.route('/author/<author_id>')
@login_required
def author(author_id):
    author = Author.query.get(author_id)
    return render_template('author.html',
                           title='search_author',
                           author=author.firstname
                           if author.surname == None
                           else f'{author.firstname} {author.surname}')

