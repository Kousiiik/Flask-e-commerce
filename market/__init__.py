from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] =os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'market.db')
app.config['SECRET_KEY']='25e5d95f9fa4a78c90e9d021'

db = SQLAlchemy(app)
Bootstrap(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)

#to redirect anonymous user to login if he want to reach login_required page
login_manager.login_view='login_page'
# to set the flash message as usual.
login_manager.login_message_category ='info'
from market import routes