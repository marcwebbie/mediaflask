import json
import os
import sys
import unittest
import urllib

import youtube_dl.YoutubeDL
import youtube_dl.extractor
from youtube_dl.utils import *
from youtube_dl.PostProcessor import FFmpegExtractAudioPP


# sys.path.append(os.path.dirname(os.path.abspath(youtube_dl.__file__)))

# General configuration(from __init__, not very elegant...)
# jar = compat_cookiejar.CookieJar()
# cookie_processor = compat_urllib_request.HTTPCookieProcessor(jar)
# proxy_handler = compat_urllib_request.ProxyHandler()
# opener = compat_urllib_request.build_opener(
#     proxy_handler, cookie_processor, YoutubeDLHandler())
# compat_urllib_request.install_opener(opener)


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


# def update_progress(morceaux, taille_morceau, taille_totale, uid=None):
#     time_now = time.time()
#     pourcent = (taille_morceau * morceaux) * 100. / taille_totale
#     sys.stderr.write("percent: {}\n".format(str(pourcent)))
#     cache.set(uid, str(pourcent))

from decorators import async
from functools import partial


@async
def download(url, disk_path, *, reporthook=None):
    name_to_save = disk_path
    if reporthook:
        urllib.request.urlretrieve(url, name_to_save, reporthook=reporthook)
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
