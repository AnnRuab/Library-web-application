from flask import Flask
from flask import redirect, render_template, request, url_for
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from config import Configuration
from itsdangerous import Signer, BadSignature
from itsdangerous.encoding import want_bytes


from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_mysqldb import MySQL

app: Flask = Flask(__name__)
app.config.from_object(Configuration)

db = MySQL()
# db: MySQL = MySQL()
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'Ann'
# app.config['MYSQL_PASSWORD'] = '0983183Ann'
# app.config['MYSQL_DB'] = 'DB2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://Ann:0983183Ann@localhost/BD2'



db.init_app(app)
db = SQLAlchemy(app)

bootstrap = Bootstrap(app)

from controllers.user import *


if __name__ == '__main__':
    app.run()
