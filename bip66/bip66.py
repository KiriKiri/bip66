from io import BytesIO


class Bip66Error (Exception):
    pass


def check(buffer):
    if len(buffer) < 8:
        return False
    if len(buffer) > 72:
        return False
    if buffer[0] != 0x30:
        return False
    if buffer[1] != len(buffer) - 2:
        return False
    if buffer[2] != 0x02:
        return False

    len_r = buffer[3]
    if len_r == 0:
        return False
    if 5 + len_r >= len(buffer):
        return False
    if buffer[4 + len_r] != 0x02:
        return False

    len_s = buffer[5 + len_r]
    if len_s == 0:
        return False
    if 6 + len_r + len_s != len(buffer):
        return False

    if buffer[4] & 0x80:
        return False
    if (len_r > 1) and (buffer[4] == 0x00) and not (buffer[5] & 0x80):
        return False

    if buffer[len_r + 6] & 0x80:
        return False
    if (len_s > 1) and (buffer[len_r + 6] == 0x00) and not (buffer[len_r + 7] & 0x80):
        return False

    return True


def decode(buffer):
    if len(buffer) < 8:
        raise Bip66Error('DER sequence length is too short')
    if len(buffer) > 72:
        raise Bip66Error('DER sequence length is too long')
    if buffer[0] != 0x30:
        raise Bip66Error('Expected DER sequence')
    if buffer[1] != len(buffer) - 2:
        raise Bip66Error('DER sequence length is invalid')
    if buffer[2] != 0x02:
        raise Bip66Error('Expected DER integer')

    len_r = buffer[3]
    if len_r == 0:
        raise Bip66Error('R length is zero')
    if 5+len_r >= len(buffer):
        raise Bip66Error('R length is too long')
    if buffer[4 + len_r] != 0x02:
        raise Bip66Error('Expected DER integer (2)')

    len_s = buffer[5 + len_r]
    if len_s == 0:
        raise Bip66Error('S length is zero')
    if 6 + len_r + len_s != len(buffer):
        raise Bip66Error('S length is invalid')

    if buffer[4] & 0x80:
        raise Bip66Error('R value is negative')
    if (len_r > 1) and (buffer[4] == 0x00) and not (buffer[5] & 0x80):
        raise Bip66Error('R value excessively padded')

    if buffer[len_r + 6] & 0x80:
        raise Bip66Error('S value is negative')
    if (len_s > 1) and (buffer[len_r + 6] == 0x00) and not (buffer[len_r + 7] & 0x80):
        raise Bip66Error('S value excessively padded')

    return buffer[4:(4 + len_r)], buffer[(6 + len_r):]


def encode(r, s):
    len_r = len(r)
    len_s = len(s)
    if len_r == 0:
        raise Bip66Error('R length is zero')

    if len_s == 0:
        raise Bip66Error('S length is zero')

    if len_r > 33:
        raise Bip66Error('R length is too long')

    if len_s > 33:
        raise Bip66Error('S length is too long')

    if r[0] & 0x80:
        raise Bip66Error('R value is negative')

    if s[0] & 0x80:
        raise Bip66Error('S value is negative')

    if len_r > 1 and (r[0] == 0x00) and not (r[1] & 0x80):
        raise Bip66Error('R value excessively padded')

    if len_s > 1 and (s[0] == 0x00) and not (s[1] & 0x80):
        raise Bip66Error('S value excessively padded')

    sign_len = 6 + len_r + len_s

    signature = BytesIO()
    signature.write(0x30.to_bytes(1, 'big', signed=False))
    signature.write((sign_len - 2).to_bytes(1, 'big', signed=False))
    signature.write(0x02.to_bytes(1, 'big', signed=False))
    signature.write(len_r.to_bytes(1, 'big', signed=False))
    signature.write(r)
    signature.write(0x02.to_bytes(1, 'big', signed=False))
    signature.write(len_s.to_bytes(1, 'big', signed=False))
    signature.write(s)

    return signature.getvalue()


