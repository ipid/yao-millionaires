__all__ = ('fast_dump', 'fast_load')
from b64utils import *
from base64 import b64encode, b64decode
from Crypto.Hash import MD5

def get_md5_msg(msg: str):
    h = MD5.new(data=msg.encode())
    return b64encode(h.digest()).decode() + ';' + msg

def unpack_md5_msg(msg: str):
    l = msg.split(';')
    assert len(l) == 2
    h = MD5.new(data=l[1].encode())
    assert l[0] == b64encode(h.digest()).decode()
    return l[1]

# Dump a list of numbers.
def fast_dump(target):
    assert len(target) > 0

    result = []
    for x in target:
        assert isinstance(x, int)
        result.append(int_b64encode(x))

    return get_md5_msg(','.join(result))

# Load a list of numbers dumped by fast_dump.
def fast_load(pack_msg):
    msg = unpack_md5_msg(pack_msg)
    assert len(msg) > 0
    l = msg.split(',')
    return [int_b64decode(x) for x in l]