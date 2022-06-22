from flask import render_template, request, redirect

import app
from app import *
from models import *

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length, Regexp

from models import Book


class LoginForm(FlaskForm):
    nickname = StringField('Нікнейм', validators=[InputRequired(message='Ім\'я не має бути порожнім!'),
                                                   Length(min=4, max=15,
                                                          message='Довжина імені має бути від 4 до 15 символів!')])
    password = PasswordField('Пароль', validators=[InputRequired(message='Пароль не має бути порожнім!'),
                                                   Length(min=4, max=10,
                                                          message='Довжина паролю має бути від 4 до 10 символів!')])
    remember = BooleanField('Запам\'ятати мене')


class SignUp(FlaskForm):
    email = StringField('Пошта',
                        validators=[Length(max=30, message='Занадто довга поштова скринька!'),
                                    Email(message='Пошта має бути заповнена!'),
                                    Regexp('^[a-z A-Z 0-9 ]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$',
                                           message='Не валідний емейл!!'), ])

    nickname = StringField('Нікнейм',
                           validators=[InputRequired(message='Ім\'я не має бути порожнім!'),
                                       Length(min=4, max=15, message='Довжина імені має бути від 4 до 15 символів!'),
                                       Regexp('[a-z A-Z а-я А-Я 0-9]+', message='Ім\'я має містити букви!')])
    password = PasswordField('Пароль',
                             validators=[InputRequired(message='Пароль не має бути порожнім!'),
                                         Length(min=4, max=10, message='Довжина паролю має бути від 4 до 10 символів!')])


@app.route('/')
def main():
    # try:
        users = db.session.query(User).all()
        print(users)
        return render_template('main.html', title='Головна сторінка')
    # except:
    #     print('problrm')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    form = SignUp()

    if current_user.is_authenticated:
        return redirect(url_for('homepage'))

    if form.validate_on_submit():
       user_datastore.create_user(password=form.password.data,
                                  email=form.email.data,
                                  nickname=form.nickname.data)
       db.session.commit()
       return redirect(url_for('login'))
    return render_template('sign_up.html', title='Реєстрація', form=form)


@app.route('/signup/homepage', methods=['POST', 'GET'])
@app.route('/login/homepage', methods=['POST', 'GET'])
@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
         return redirect(url_for('homepage'))

    form = LoginForm()
    if form.validate_on_submit():
         user = User.query.filter_by(nickname=form.nickname.data).first()
         if user:
             if user.password == form.password.data:
                 login_user(user, remember=form.remember.data)
                 return redirect(url_for('homepage'))
    return render_template('sequrity/login_user.html', title='Увійти', form=form)


from app import db

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)



@app.route('/search')
@login_required
def search():
    q = request.args.get('q')
    if q:
        book = db.session.query(Book).filter(Book.name.ilike(('%{0}%').format(q))).all()
        author = db.session.query(Author).filter(Author.firstname.ilike(('%{0}%').format(q))
                                                  | Author.surname.ilike(('%{0}%').format(q))).all()
        return render_template('search_res.html',
                               title='search',
                               book=book,
                               author=author)
    else:
        genres = Genre.query.all()
        return render_template('search.html',
                               title='search',
                               user_id=current_user.id,
                               genres=genres)


@app.route('/library')
@login_required
def library():
    user_id = current_user.id
    songs = db.session.query(Book).filter(Book.users.any(User.id == user_id))
    return render_template('library.html',
                           title='library',
                           songs=songs,
                           author=Author)


@app.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    books = db.session.query(Book).filter(Book.users.any(User.id == current_user.id))
    count = books.count()
    return render_template('profile.html',
                           title='profile',
                           user=current_user,
                           count=count,
                           books=Book,
                           author=Author,
                           flag=True)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))