"""
    common
    ~~~~~~
    :copyright: (c) 2018 by Taffy.
"""

def md5(str):
    import hashlib
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()