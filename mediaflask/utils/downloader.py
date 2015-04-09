import urllib

import requests
from youtube_dl import YoutubeDL

from .decorators import async


BUF_SIZE = 1024


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
    total_size = int(lower_headers['content-length'].strip())
    downloaded_size = 0

    with open(destination_path, "wb") as f:
        for buf in res.iter_content(BUF_SIZE):
            if buf:
                f.write(buf)
                downloaded_size += len(buf)
                reporthook(downloaded_size, total_size)


def info(url):
    return YoutubeDL().extract_info(url, download=False)
