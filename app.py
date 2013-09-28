import datetime
import os
from uuid import uuid4

from flask import Flask, Response, render_template, redirect, url_for, request
from flask import g
from peewee import *


DATABASE = 'mediaflask.db'
DEBUG = True
SECRET_KEY = 'hin6bab8ge25*r=x&amp;+5$0kn=-#log$pt^#@vrqjld!^2ci@g*b'

app = Flask(__name__)
app.config.from_object(__name__)

database = SqliteDatabase(DATABASE)


class BaseModel(Model):

    class Meta:
        database = database


class Audiofile(BaseModel):
    uid = TextField(primary_key=True, default=lambda: str(uuid4()))
    title = TextField()
    dl_percent = IntegerField()
    dl_date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        order_by = ('-dl_date',)


def create_tables():
    database.connect()
    Audiofile.create_table()


def fetch_json_info():
    pass

app.secret_key = 'development key'


@app.before_request
def before_request():
    g.db = database
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/check", methods=['POST'])
def check():
    import downloader
    if request.method == 'POST':
        # import pdb
        # pdb.set_trace()
        json_info = downloader.info(request.form["url"])
    return Response(json_info, mimetype='text/json')


# @app.route('/user')
# def show_user_profile(url):
# import pdb
# pdb.set_trace()
# show the user profile for that user
#     return 'User %s' % username

# @app.route("/new", methods=['GET', 'POST'])
# def new_post():
#     if request.method == 'POST':
#         title = request.form["post_title"]
#         content = request.form["post_content"]
#         Message.create(title=title, content=content)
#         return redirect(url_for('home'))
#     return render_template('skl_new_post.html')


# @app.route("/detail/<post_id>")
# def detail(post_id):
#     message = Message.get(id=post_id)
#     return render_template('skl_detail.html', msg=message)


# @app.route("/supprimer/<post_id>")
# def supprimer(post_id):
#     message = Message.get(id=post_id)
#     message.delete_instance()
#     return redirect(url_for('home'))


if __name__ == "__main__":
    if not os.path.exists(DATABASE):
        print("Creation de la base de données...")
        create_tables()
        print("Base de données crée...")
    app.run()
