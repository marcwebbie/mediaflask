import datetime
from functools import partial
import glob
import json
import os
import sys
import time
import urllib.request
from uuid import uuid4

from flask import Flask, Response, render_template, redirect, url_for, request, send_file
from flask import g
from peewee import *
from werkzeug.contrib.cache import SimpleCache
from pydub import AudioSegment

from downloader import download as save_video
from downloader import info

cache = SimpleCache()
# messages on cache must be formated like that:
# {
#     'uid': '5151-5156-15115615-1515',
#     'dl_progress': 10,
#     'convert_progress': 0,
# 'status': 'converting',   # dowloading, converting, done
# }

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media/')
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
    raw_url = TextField()
    extension = TextField()
    disk_path = TextField(default="")

    class Meta:
        order_by = ('-extension',)

    def export(self, output_format='mp3'):
        af_audio_path = os.path.join(MEDIA_ROOT, "{}.{}".format(
            self.disk_path.strip('.' + self.extension), output_format))
        AudioSegment.from_file(self.disk_path).export(af_audio_path, format=output_format)
        return af_audio_path


def update_progress(morceaux, taille_morceau, taille_totale, uid=None):
    pourcent = (taille_morceau * morceaux) * 100. / taille_totale
    sys.stderr.write("percent: {}\n".format(str(pourcent)))
    if uid:
        json_report = {
            'uid': uid,
            'dl_progress': pourcent,
            'convert_progress': 0,
            'status': 'downloading',   # dowloading, converting, done
        }
        cache.set(uid, json.dumps(json_report))

# from decorators import async
# from functools import partial


# @async
# def save_video(audiofile_uid, url, disk_path, extension):
#     name_to_save = disk_path
#     rh = partial(update_progress, uid=audiofile_uid)
#     urllib.request.urlretrieve(url, name_to_save, reporthook=rh)


# def info(url):
#     import sys
#     import shlex
#     import subprocess
#     from tempfile import NamedTemporaryFile
#     import os
#     import re
#     import json

#     with NamedTemporaryFile('w+t', suffix='.info.json') as f:
#         cmd_dl = "youtube-dl {} --write-info-json --skip-download -f mp4 -q -o {}".format(
#             url, re.sub("\.info\.json", "", f.name))
#         with subprocess.Popen(shlex.split(cmd_dl)) as ydl:
#             pass
#         info = f.read()
#         return info


def create_tables():
    database.connect()
    Audiofile.create_table()


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
        ext = info_dict['ext']
        raw_url = info_dict['url']
        af = Audiofile.create(extension=ext, raw_url=raw_url)

        # add uid to dict for json
        info_dict['uid'] = af.uid
        info_json = json.dumps(info_dict)

    return Response(info_json, mimetype='application/json')


@app.route("/progress/<uid>")
def progress(uid):
    info_dict = json.loads(cache.get(uid))
    # if int(info_dict['dl_progress']) >= 100:
    #     info_dict['status'] = 'done'
    #     json_info = json.dumps(info_dict)
    #     return Response(json_info, mimetype='application/json')
    return Response(cache.get(uid), mimetype='application/json')


@app.route("/convert/<uid>", methods=['GET'])
def convert(uid):
    af = Audiofile.select().where(Audiofile.uid == uid).get()
    audiofile_uid = af.uid
    url = af.raw_url
    ext = af.extension
    af.disk_path = os.path.join(MEDIA_ROOT, "{}.{}".format(uid, ext))
    af.save()

    rh = partial(update_progress, uid=audiofile_uid)
    save_video(url, af.disk_path, reporthook=rh)
    return Response(url_for("progress", uid=uid), mimetype='text/plain')


@app.route("/download/<uid>")
def download(uid):
    af = Audiofile.select().where(Audiofile.uid == uid).get()
    af_audio_path = af.export('mp3')
    return send_file(af_audio_path, as_attachment=True, mimetype='video/mpeg')


def clear_server():
    if os.path.exists(DATABASE):
        print("Supprimer la base de données...")
        os.remove(DATABASE)
    print("Supprimer fichiers multimedia...")
    for f in glob.glob(os.path.join(MEDIA_ROOT, '*')):
        os.remove(f)

if __name__ == "__main__":
    clear_server()
    print("Creation de la base de données...")
    create_tables()
    print("Base de données crée...")
    app.run()
