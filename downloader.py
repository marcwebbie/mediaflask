import sys
import urllib
import time


class Reporter(object):

    def __init__(self, time_debut):
        self.initial = time_debut

    def humanize_bytes(self, byt, precision=1):
        abbrevs = (
            (1 << 50, 'PB'),
            (1 << 40, 'TB'),
            (1 << 30, 'GB'),
            (1 << 20, 'MB'),
            (1 << 10, 'kB'),
            (1, 'bytes')
        )
        if byt == 1:
            return '1 byte'
        for factor, suffix in abbrevs:
            if byt >= factor:
                break
        return '%.*f %s' % (precision, byt / factor, suffix)

    def __call__(self, morceaux, taille_morceau, taille_totale):
        time_now = time.time()
        pourcent = (taille_morceau * morceaux) * 100. / taille_totale
        diff = int(time_now - self.initial)
        vitesse = (taille_morceau * morceaux / diff) if diff else diff
        # sys.stdout.write(
        #     "\r[%3.2f%%] %s> %100s [%s b/s]" % (
        #         pourcent,
        #         "-" * int(
        #     pourcent),
        #         '',
        #         self.humanize_bytes(
        #         vitesse)))
        sys.stdout.write("\r[{}%]".format(int(pourcent)))
        sys.stdout.flush()

# class video_downloader(object):
#     def __init__(self, options_passed):
#         ''' Contructor needs options as a list'''
#         self.opts = options_passed
#     def download(self, title, name_to_save, url):
#         print title, '->', name_to_save
#         reporthook = Reporter(time.time())
#         urllib.urlretrieve(url, name_to_save, reporthook)
#     def extract_info(self, link, handler):
# get video raw info
#         video_raw_info = handler(link)
# Use the raw info to open a file for writing
#         url = video_raw_info['url']
#         title = video_raw_info['title']
#         video_format = video_raw_info['extension']
#         video_path = video_raw_info['video_path']
#         name_to_save = ''
#         self.download(title, name_to_save, url)


def download(title, name_to_save, url):
    import urllib.request
    # print title, '->', name_to_save
    rh = Reporter(time.time())
    urllib.request.urlretrieve(url, name_to_save, reporthook=rh)


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
        # info = json.loads(f.read())
        info = f.read()
        # import pdb
        # pdb.set_trace()

        return info
        # print("downloading: {}...".format(info['fulltitle']))
        # title = info['fulltitle']
        # raw_url = info['url']

        # Create temp file for download
        # with NamedTemporaryFile('w+t') as dl_file:
        #     download(title, dl_file.name, raw_url)

if __name__ == "__main__":
    url = sys.argv[1]
    print(info(url))
