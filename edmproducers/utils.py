import hashlib
import os
from functools import partial


def hash_file(file, block_size=65536):
    m = hashlib.md5()
    for buf in iter(partial(file.read, block_size), b''):
        m.update(buf)

    return m.hexdigest()


def upload_track_to(instance, filename):
    instance.track.file.open()
    filename_base, filename_ext = os.path.splitext(filename)
    return "{0}{1}".format('tracks' + os.sep + hash_file(instance.track.file), filename_ext)
