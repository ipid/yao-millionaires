__all__ = ('int_b64encode', 'int_b64decode')
from base64 import b64decode, b64encode

def int_b64encode(x: int):
    xbyte = x.to_bytes((x.bit_length() + 7) // 8, byteorder='big')
    return b64encode(xbyte).decode()

def int_b64decode(x: str):
    return int.from_bytes(b64decode(x.encode()), byteorder='big')