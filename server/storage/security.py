from codecs import encode, decode

import bcrypt

def hash_password(password):
    return decode(bcrypt.hashpw(encode(password, "utf-8"), bcrypt.gensalt()), "utf-8")

def check_password(password, hashed):
    return bcrypt.checkpw(encode(password, "utf-8"), encode(hashed, "utf-8"))
