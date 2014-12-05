import urllib

import requests
import youtube_dl.YoutubeDL
import youtube_dl.extractor
from youtube_dl.utils import *

from .decorators import async


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


@async
def download(url, disk_path, reporthook=None):
    name_to_save = disk_path
    if reporthook:
        urllib.request.urlretrieve(url, name_to_save, reporthook=reporthook)
    else:
        urllib.request.urlretrieve(url, name_to_save, reporthook=reporthook)


@async
def save(url, destination_path, reporthook):
    res = requests.get(url, stream=True)
    lower_headers = {k.lower(): res.headers[k] for k in res.headers.keys()}
    # import pdb;pdb.set_trace()
    total_size = int(lower_headers['content-length'].strip())
    downloaded_size = 0

    with open(destination_path, "wb") as f:
        BUF_SIZE = 1024
        for buf in res.iter_content(BUF_SIZE):
            if buf:
                f.write(buf)
                downloaded_size += len(buf)
                reporthook(downloaded_size, total_size)


def info(url):
    params = {}
    params['quiet'] = True
    params['writeinfojson'] = True
    params['skip_download'] = True
    params['outtmpl'] = 'temp'
    ytb = youtube_dl.YoutubeDL(params)
    info_dict = ytb.extract_info(url)
    return info_dict

    # yexts = [ie for ie in ytb._ies if ie.suitable(url)]
    # jsonpath = params['outtmpl'] + '.info.json'
    # open(jsonpath, 'wb').close()
    # youtube_dl.YoutubeDL(params).download([url])

    # info = open(jsonpath, 'r').read()
    # os.remove(jsonpath)

    # return info

    # with NamedTemporaryFile('w+t', suffix='.info.json') as json_file:
    #     params['outtmpl'] = re.sub("\.info\.json", "", json_file.name)
    #     ydl = youtube_dl.YoutubeDL(params)
    #     ydl.add_default_info_extractors()
    #     ydl.download([url])

    #     import pdb; pdb.set_trace()
    #     info = json_file.read()
    #     return info
