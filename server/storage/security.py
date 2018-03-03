from codecs import encode, decode

import bcrypt


def hash_password(password):
    salted = bcrypt.hashpw(encode(password, "utf-8"), bcrypt.gensalt())
    return decode(salted, "utf-8")


def check_password(password, hashed):
    return bcrypt.checkpw(encode(password, "utf-8"), encode(hashed, "utf-8"))
