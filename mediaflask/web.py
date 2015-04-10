# -*- coding: utf-8 -*-
import json
import os
import shutil
import sys

from flask import (
    Flask,
    Response,
    render_template,
    request,
    send_from_directory,
)
from werkzeug.contrib.cache import SimpleCache
from pydub import AudioSegment
from slugify import slugify_unicode as slugify

from mediaflask.utils import downloader
from mediaflask.audiofile import AudioFile

app = Flask(__name__)
app.debug = False
cache = SimpleCache()
MEDIA_ROOT = os.path.expanduser("~/.mediaflask")


def update_progress(downloaded_size, total_size):
    dl_progress = downloaded_size * 100. / total_size
    if app.debug:
        sys.stderr.write("\rprogress: {}%".format(str(dl_progress)))
    cache.set("dl_progress", dl_progress)


@app.route("/progress")
def progress():
    dl_progress = cache.get("dl_progress")
    return str(dl_progress)


@app.route("/download", methods=['POST'])
def download():
    if request.method == 'POST':
        output_format = request.form['song_format_input']
        audio_tags = {
            'artist': request.form['artist_input'],
            'title': request.form['song_title_input'],
            'album': request.form['album_input'],
            'date': request.form['year_input'],
        }

        audiofile = cache.get("audiofile")
        audio_segment = AudioSegment.from_file(audiofile.disk_path)
        audio_output_path = "{}.{}".format(
            os.path.join(MEDIA_ROOT, audiofile.slug),
            output_format
        )
        audio_segment.export(
            audio_output_path,
            format=output_format,
            tags=audio_tags,
            id3v2_version='3'
        )

        return send_from_directory(
            MEDIA_ROOT,
            os.path.basename(audio_output_path),
            as_attachment=True,
        )


@app.route("/convert")
def convert():
    audiofile = cache.get("audiofile")
    url = audiofile.raw_url
    disk_path = audiofile.disk_path
    rh = update_progress
    downloader.save(url, disk_path, reporthook=rh)
    return "OK"


@app.route("/check", methods=["POST"])
def check():
    if request.method == 'POST':
        url = request.form["url"]
        info_dict = downloader.info(url)
        title = info_dict['title']
        extension = info_dict['ext']
        raw_url = info_dict['url']
        thumbnail = info_dict["thumbnail"]
        slug = slugify(title)
        disk_path = os.path.join(MEDIA_ROOT, slug)
        audiofile = AudioFile(
            title=title,
            extension=extension,
            url=url,
            raw_url=raw_url,
            thumbnail=thumbnail,
            slug=slug,
            disk_path="{}.{}".format(disk_path, extension)
        )
        cache.set("audiofile", audiofile)
        info_json = json.dumps(info_dict)
    return Response(info_json, mimetype='application/json')


@app.route("/")
def home():
    return render_template('home.html')


def create_media_dir(mediapath):
    if not os.path.exists(mediapath):
        os.makedirs(mediapath)


def remove_media_dir(mediapath):
    shutil.rmtree(mediapath, ignore_errors=True)


def main():
    create_media_dir(MEDIA_ROOT)
    try:
        app.run(debug=True)
    except Exception as e:
        raise e
    finally:
        remove_media_dir(MEDIA_ROOT)


if __name__ == "__main__":
    main()
