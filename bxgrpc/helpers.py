#encoding=utf-8

import hashlib
import re

def convert2uint(data):
    m = hashlib.md5()
    m.update(data.encode('utf-8'))
    md5_str = m.hexdigest()
    return int(md5_str[:16], 16)

def is_standard_tag(tags=[]):
    if not tags:
        return False

    return True
