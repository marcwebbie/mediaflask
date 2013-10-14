import json
import os
import sys
from tempfile import NamedTemporaryFile
import unittest
import urllib

from pydub import AudioSegment

import youtube_dl.YoutubeDL
import youtube_dl.extractor
from youtube_dl.utils import *
from youtube_dl.PostProcessor import FFmpegExtractAudioPP

params = {
    "consoletitle": False,
    "continuedl": True,
    "forcedescription": False,
    "forcefilename": False,
    "forceformat": False,
    "forcethumbnail": False,
    "forcetitle": False,
    "forceurl": False,
    "format": None,
    "format_limit": None,
    "ignoreerrors": False,
    "listformats": None,
    "logtostderr": False,
    "matchtitle": None,
    "max_downloads": None,
    "nooverwrites": False,
    "nopart": False,
    "noprogress": False,
    "outtmpl": "%(id)s.%(ext)s",
    "password": None,
    "playlistend": -1,
    "playliststart": 1,
    "prefer_free_formats": False,
    "quiet": False,
    "ratelimit": None,
    "rejecttitle": None,
    "retries": 10,
    "simulate": False,
    "skip_download": False,
    "subtitleslang": None,
    "subtitlesformat": "srt",
    "test": False,
    "updatetime": True,
    "usenetrc": False,
    "username": None,
    "verbose": True,
    "writedescription": False,
    "writeinfojson": False,
    "writesubtitles": False,
    "allsubtitles": False,
    "listssubtitles": False
}


from functools import partial
from threading import Thread
import multiprocessing


def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper


def multiprocessed(func):
    def wrapper(*args, **kwargs):
        p = multiprocessing.Process(target=func, args=args, kwargs=kwargs)
        p.start()
    return wrapper


@async
def download(url, disk_path, export='mp3', bitrate='192', tags=None, reporthook=None):
    name_to_save = disk_path
    if export:
        with NamedTemporaryFile('w+t') as temp_video_file:
            urllib.request.urlretrieve(url, temp_video_file.name, reporthook=reporthook)
            AudioSegment.from_file(temp_video_file.name).export(
                name_to_save,
                format=export,
                bitrate=bitrate,
                tags=tags,
                # error replace cmd join in pydub with str(v) for v in value_list
                id3v2_version=u'3'
            )

        # notify user of end of download
        import shlex
        import subprocess
        notify_cmd = 'notify-send "Download completed!" "{0}" --icon=dialog-information'.format(
            name_to_save)
        subprocess.call(shlex.split(notify_cmd))
    else:
        urllib.request.urlretrieve(url, name_to_save, reporthook=reporthook)


def info(url):
    from tempfile import NamedTemporaryFile
    import re

    params['quiet'] = True
    params['writeinfojson'] = True
    params['skip_download'] = True

    with NamedTemporaryFile('w+t', suffix='.info.json') as json_file:
        params['outtmpl'] = re.sub("\.info\.json", "", json_file.name)
        ydl = youtube_dl.YoutubeDL(params)
        ydl.add_default_info_extractors()
        ydl.download([url])

        info = json_file.read()
        return info
