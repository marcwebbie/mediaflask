import datetime
import json
import os
from uuid import uuid4
import urllib.request
import sys
import time

from flask import Flask, Response, render_template, redirect, url_for, request
from flask import g
from peewee import *
from werkzeug.contrib.cache import SimpleCache


cache = SimpleCache()

DATABASE = 'mediaflask.db'
DEBUG = True
SECRET_KEY = 'hin6bab8ge25*r=x&amp;+5$0kn=-#log$pt^#@vrqjld!^2ci@g*b'

app = Flask(__name__)
app.config.from_object(__name__)
database = SqliteDatabase(DATABASE, check_same_thread=False)


class BaseModel(Model):

    class Meta:
        database = database


class Audiofile(BaseModel):
    uid = TextField(primary_key=True, default=lambda: str(uuid4()))
    json = TextField(null=True)
    dl_progress = IntegerField(default=0)
    dl_date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        order_by = ('-dl_date',)

    @property
    def disk_path():
        return


def update_progress(morceaux, taille_morceau, taille_totale, uid=None):
    time_now = time.time()
    pourcent = (taille_morceau * morceaux) * 100. / taille_totale
    sys.stderr.write("percent: {}\n".format(str(pourcent)))
    cache.set(uid, str(pourcent))

from decorators import async
from functools import partial


@async
def save_video(audiofile, url, disk_path, extension):
    name_to_save = disk_path
    uid = audiofile.uid
    rh = partial(update_progress, uid=uid)
    urllib.request.urlretrieve(url, name_to_save, reporthook=rh)
    audiofile.dl_date = datetime.datetime.now()
    audiofile.save()


def info(url):
    import sys
    import shlex
    import subprocess
    from tempfile import NamedTemporaryFile
    import os
    import re
    import json

    with NamedTemporaryFile('w+t', suffix='.info.json') as f:
        cmd_dl = "youtube-dl {} --write-info-json --skip-download -f mp4 -q -o {}".format(
            url, re.sub("\.info\.json", "", f.name))
        with subprocess.Popen(shlex.split(cmd_dl)) as ydl:
            pass
        info = f.read()
        return info


def create_tables():
    database.connect()
    Audiofile.create_table()


def fetch_json_info():
    pass


def fake_download(audiofile, ext):
    import time
    import sys
    percent = 0
    while percent < 100:
        sys.stderr.write(str(percent))
        percent += 5
        time.sleep(1)

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
    if request.method == 'POST':
        url = request.form["url"]
        info_json = info(url)
        info_dict = json.loads(info_json)
        af = Audiofile.create(url=url, json=info_json)

        # add uid to dict for json
        info_dict['uid'] = af.uid
        info_json = json.dumps(info_dict)

    return Response(info_json, mimetype='application/json')


@app.route("/progress/<uid>")
def progress(uid):
    return Response(cache.get(uid), mimetype='text/plain')


@app.route("/download/<uid>")
def download(uid):
    af = Audiofile.select().where(Audiofile.uid == uid).get()
    info_dict = json.loads(af.json)
    url = info_dict['url']
    ext = info_dict['ext']
    disk_path = "{}.{}".format(uid, ext)

    save_video(af, url, disk_path, ext)
    return Response(url_for("progress", uid=uid), mimetype='text/plain')


if __name__ == "__main__":
    if not os.path.exists(DATABASE):
        print("Creation de la base de données...")
        create_tables()
        print("Base de données crée...")
    app.run()
