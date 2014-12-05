from collections import namedtuple

AudioFile = namedtuple(
    "AudioFile",
    ["title", "extension", "url", "raw_url", "thumbnail", "slug", "disk_path"]
)
